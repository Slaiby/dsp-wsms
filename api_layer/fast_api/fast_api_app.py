import json
from fastapi import FastAPI, UploadFile, File, Depends
from typing import List, Dict, Union
import pandas as pd

from api_layer.fast_api.service_slices import fetch_past_predictions, handle_csv_file, insert_inference_data
from logic_layer.acceptance_prediction.csv_service import validate_csv
from logic_layer.acceptance_prediction.inference import PredictionModel
from logic_layer.pydantic_models import Prediction, PredictionRequest

app = FastAPI()

predictor = PredictionModel()

async def get_predictor():
    return predictor

@app.post("/predict")
async def predict(request_data: Union[PredictionRequest, Dict], predictor: PredictionModel = Depends(get_predictor)):
    input_dict = request_data.model_dump() if isinstance(request_data, PredictionRequest) else request_data
    prediction = predictor.make_prediction(input_dict)
    await insert_inference_data(input_dict, prediction.tolist()[0])
    return {"prediction": prediction.tolist()}

@app.get("/get-past-predictions", response_model=List[Prediction])
async def get_past_predictions_endpoint():
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
    file_in_memory = await handle_csv_file(file)
    is_valid, message = validate_csv(file_in_memory)
    return {"filename": file.filename, "is_valid": is_valid, "message": message}

@app.post("/predict_from_csv")
async def predict_from_csv(file: UploadFile = File(...)):
    file_in_memory = await handle_csv_file(file)
    df = pd.read_csv(file_in_memory)

    predictions = [predictor.make_prediction(row.to_dict()).tolist()[0] for _, row in df.iterrows()]
    return {"predictions": predictions}
