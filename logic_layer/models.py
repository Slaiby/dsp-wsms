from pydantic import BaseModel

class Prediction(BaseModel):
    id: int
    inference_id: str
    result: dict 
    timestamp: str
    
class PredictionRequest(BaseModel):
    credit_history: float
    dependents: str
    education: str
    married: str
    property_area: int
    coapplicant_income: float