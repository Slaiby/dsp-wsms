from fastapi import FastAPI
from typing import List
import json
import numpy as np

from api_layer.fast_api.service_slices import fetch_past_predictions
from logic_layer.pydantic_models import Prediction, PredictionRequest
from logic_layer.acceptance_prediction.inference import make_predictions

app = FastAPI()

@app.post("/predict")
async def predict(request_data: PredictionRequest):
    input_dict = request_data.model_dump()
    prediction = make_predictions(input_dict)
    return {"prediction": prediction.tolist()}

@app.get("/get-past-predictions", response_model=List[Prediction])
async def get_past_predictions():
    predictions = await fetch_past_predictions()
    prediction_list = [Prediction(
        id=row['id'],
        inference_id=row['inference_id'],
        result=json.loads(row['result']) if isinstance(row['result'], str) else row['result'],
        timestamp=row['timestamp'].isoformat()
    ) for row in predictions]
    return prediction_list