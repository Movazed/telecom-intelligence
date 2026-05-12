import pandas as pd
import numpy as np
from sklearn.ensemble import RandomForestClassifier
import joblib

def final_retrain():
    # Generate 5000 diverse samples to cover all scenarios
    np.random.seed(42)
    n = 5000
    data = {
        'avg_usage': np.random.uniform(100, 6000, n),
        'growth_rate': np.random.uniform(-0.2, 0.8, n),
        'variability': np.random.uniform(0.0, 1.0, n),
        'peak_ratio': np.random.uniform(1.0, 4.0, n)
    }
    df = pd.DataFrame(data)

    # Stricter labeling for UI demonstration
    def label_risk(row):
        if row['avg_usage'] > 4000 and row['variability'] > 0.7:
            return 2 # HIGH
        if row['avg_usage'] > 1800:
            return 1 # MEDIUM
        return 0     # LOW

    df['target'] = df.apply(label_risk, axis=1)
    
    # Train on named features to match the predict.py fix
    feature_cols = ['avg_usage', 'growth_rate', 'peak_ratio', 'variability']
    X = df[feature_cols]
    y = df['target']
    
    model = RandomForestClassifier(n_estimators=100)
    model.fit(X, y)
    
    joblib.dump(model, 'ml/model.pkl')
    print("Final Model Saved. ")

if __name__ == "__main__":
    final_retrain()