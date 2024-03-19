from pydantic import BaseModel


class Prediction(BaseModel):
    id: int
    inference_id: str
    result: dict 
    timestamp: str