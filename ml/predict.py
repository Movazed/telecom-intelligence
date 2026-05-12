import joblib
import pandas as pd
import numpy as np
import os

MODEL_PATH = 'ml/model.pkl'

def predict_usage_risk(features_dict: dict) -> dict:
    try:
        if not os.path.exists(MODEL_PATH):
            return {"error": "Model file not found. Run training script first."}
            
        model = joblib.load(MODEL_PATH)
        
        # Convert dict to DataFrame with explicit column names to avoid warnings
        input_df = pd.DataFrame([{
            'avg_usage': float(features_dict.get('avg_usage', 0)),
            'growth_rate': float(features_dict.get('growth_rate', 0)),
            'peak_ratio': float(features_dict.get('peak_ratio', 1.5)),
            'variability': float(features_dict.get('variability', 0))
        }])
        
        # Ensure strict column order
        feature_cols = ['avg_usage', 'growth_rate', 'peak_ratio', 'variability']
        input_df = input_df[feature_cols]
        
        prediction = int(model.predict(input_df)[0])
        score = float(model.predict_proba(input_df).max())
        
        risk_map = {0: "LOW", 1: "MEDIUM", 2: "HIGH"}
        
        return {
            "congestion_risk": risk_map[prediction],
            "anomaly_flag": True if prediction == 2 else False,
            "score": score
        }
    except Exception as e:
        return {"error": str(e)}