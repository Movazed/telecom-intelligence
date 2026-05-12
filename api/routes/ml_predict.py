from fastapi import APIRouter, HTTPException
from api.schemas import PredictionRequest, PredictionResponse
from ml.predict import predict_usage_risk

router = APIRouter()

# Updated the path to exactly match what the React frontend is calling
@router.post("/predict-usage-risk", response_model=PredictionResponse)
def predict_risk(request: PredictionRequest):
    features = request.dict()
    result = predict_usage_risk(features)
    
    if "error" in result:
        raise HTTPException(status_code=500, detail=result["error"])
        
    return result