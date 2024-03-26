from fastapi import FastAPI
from typing import List
import os
import json
import numpy as np
from fastapi import FastAPI, UploadFile, File, HTTPException

from api_layer.fast_api.service_slices import fetch_past_predictions, insert_inference_data
from logic_layer.pydantic_models import Prediction, PredictionRequest
from logic_layer.acceptance_prediction.inference import make_predictions

app = FastAPI()

UPLOAD_FOLDER = os.path.abspath(os.path.join(os.path.dirname(__file__), "..", "..", "Airflow-dag-pipeline", "uploaded-files"))

# Maximum allowed file size (200MB)
MAX_FILE_SIZE_BYTES = 200 * 1024 * 1024


@app.post("/predict")
async def predict(request_data: PredictionRequest):
    input_dict = request_data.model_dump()
    prediction = make_predictions(input_dict)
    await insert_inference_data(input_dict, prediction.tolist()[0])
    return {"prediction": prediction.tolist()}

@app.get("/get-past-predictions", response_model=List[Prediction])
async def get_past_predictions():
    predictions = await fetch_past_predictions() 
    prediction_list = [
        Prediction(
            id=prediction['id'],
            result=json.loads(prediction['request_data']),
            prediction=str(prediction['prediction']),
            timestamp=str(prediction['timestamp'])
        ) for prediction in predictions     
    ]
    return prediction_list

@app.post("/file/upload")
async def create_upload_file(file: UploadFile = File(...)):
    if not file.filename.endswith(".csv"):
        raise HTTPException(status_code=400, detail="File must be CSV")

    file_size = os.fstat(file.file.fileno()).st_size
    if file_size > MAX_FILE_SIZE_BYTES:
        raise HTTPException(status_code=413, detail="File size exceeds maximum limit")

    if not os.path.exists(UPLOAD_FOLDER):
        os.makedirs(UPLOAD_FOLDER)

    file_path = os.path.join(UPLOAD_FOLDER, file.filename)
    with open(file_path, "wb") as buffer:
        buffer.write(await file.read())

    return {"filename": file.filename, "file_path": file_path}