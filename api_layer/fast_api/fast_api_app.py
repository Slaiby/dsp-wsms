from fastapi import FastAPI
from typing import List

from api_layer.fast_api.service_slices import fetch_past_predictions
from logic_layer.models import Prediction

app = FastAPI()

@app.post("/predict")
async def predict():
    return {"message": "Hello, FastAPI!"}

@app.get("/get-past-predictions", response_model=List[Prediction])
async def get_past_predictions():
    predictions = await fetch_past_predictions()
    return [Prediction(
        id=row['id'],
        inference_id=row['inference_id'],
        result=row['result'],
        timestamp=row['timestamp'].isoformat()
    ) for row in predictions]