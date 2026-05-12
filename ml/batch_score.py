import pandas as pd
import joblib
import os

def run_batch_scoring():
    """Task 6.6: Batch Scoring """
    print("Starting batch scoring process...")
    
    # 1. Load the model
    model = joblib.load('ml/model.pkl')
    
    # 2. Load the features (using the same logic as our trainer)
    df = pd.read_parquet('data/processed/telecom_usage/')
    features = df.groupby('grid_id').agg(
        avg_usage=('internet_usage', 'mean'),
        variability=('internet_usage', 'std')
    ).fillna(0).reset_index()
    
    # Mocking growth_rate and peak_ratio to match training schema
    features['growth_rate'] = 0.05 
    features['peak_ratio'] = 1.5
    
    # 3. Run predictions
    X = features[['avg_usage', 'growth_rate', 'peak_ratio', 'variability']]
    features['congestion_risk_score'] = model.predict(X)
    
    risk_map = {0: "LOW", 1: "MEDIUM", 2: "HIGH"}
    features['risk_label'] = features['congestion_risk_score'].map(risk_map)
    
    # 4. Save results 
    output_path = 'ml/batch_predictions.csv'
    features[['grid_id', 'risk_label']].to_csv(output_path, index=False)
    print(f"✅ Batch scoring complete! Results saved to {output_path}")

if __name__ == "__main__":
    run_batch_scoring()