from pydantic import BaseModel

class Prediction(BaseModel):
    id: int
    result: dict
    prediction: float
    timestamp: str
    
class PredictionRequest(BaseModel):
    ApplicantIncome: float
    CoapplicantIncome: float
    LoanAmount: float
    Loan_Amount_Term: float
    Credit_History: float
    Dependents: str
    Education: str
    Married: str
    Property_Area: str