import pandas as pd
import pickle
import numpy as np

def score_vessel_data(df):
    """Add anomaly score to dataframe using trained model."""
    # Load model and feature names
    with open('enhanced_model.pkl', 'rb') as f:
        model = pickle.load(f)
    with open('feature_names.pkl', 'rb') as f:
        feature_columns = pickle.load(f)
    
    # Prepare features (same as training)
    df = df.copy()
    df['course_change'] = df.groupby('vessel_id')['course'].diff().fillna(0).abs()
    df['course_change'] = df['course_change'].apply(lambda x: min(x, 360-x))
    
    # Ensure all required columns exist
    for col in feature_columns:
        if col not in df.columns:
            df[col] = 0
    
    X = df[feature_columns].fillna(0).values
    
    # Get anomaly score: negative score = more anomalous
    # Convert to 0-1 range where 1 = most anomalous
    scores = model.decision_function(X)  # more negative = anomalous
    # Normalize to 0-1 (higher = more anomalous)
    min_score, max_score = scores.min(), scores.max()
    anomaly_scores = (max_score - scores) / (max_score - min_score)
    anomaly_scores = np.clip(anomaly_scores, 0, 1)
    
    df['anomaly_score'] = anomaly_scores
    df['is_anomaly'] = (df['anomaly_score'] > 0.6).astype(int)  # threshold
    
    return df

# Example usage
if __name__ == '__main__':
    sample = pd.read_csv('enhanced_vessel_data.csv').head(10)
    scored = score_vessel_data(sample)
    print(scored[['vessel_id', 'speed', 'anomaly_score', 'is_anomaly']])