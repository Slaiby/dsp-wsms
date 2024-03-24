from fastapi import FastAPI
from typing import List
import json
import numpy as np

from api_layer.fast_api.service_slices import fetch_past_predictions, insert_inference_data
from logic_layer.pydantic_models import Prediction, PredictionRequest
from logic_layer.acceptance_prediction.inference import make_predictions

app = FastAPI()

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