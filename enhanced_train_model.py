import pandas as pd
import numpy as np
from sklearn.ensemble import IsolationForest
import pickle

# Load data
df = pd.read_csv('enhanced_vessel_data.csv')

# Feature engineering
df['timestamp'] = pd.to_datetime(df['timestamp'])

# Create additional derived features
df['speed_zscore'] = (df['speed'] - df.groupby('vessel_type')['speed'].transform('mean')) / df.groupby('vessel_type')['speed'].transform('std')
df['course_change'] = df.groupby('vessel_id')['course'].diff().fillna(0).abs()
df['course_change'] = df['course_change'].apply(lambda x: min(x, 360-x))  # smallest angle

# Select features for training
feature_columns = [
    'speed',
    'acceleration',
    'heading_rate',
    'distance_to_shipping_lane_nm',
    'distance_to_port_nm',
    'time_since_last_ais_sec',
    'course_change'
]

# Fill any NaNs (first record has no course change)
df[feature_columns] = df[feature_columns].fillna(0)

X = df[feature_columns].values

# Train Isolation Forest (assume 5% anomalies)
model = IsolationForest(contamination=0.05, random_state=42, n_estimators=100)
model.fit(X)

# Save model and feature names
with open('enhanced_model.pkl', 'wb') as f:
    pickle.dump(model, f)

# Save feature names for later use
with open('feature_names.pkl', 'wb') as f:
    pickle.dump(feature_columns, f)

# Evaluate on training data (just for info)
df['predicted_anomaly'] = model.predict(X)
df['predicted_anomaly'] = df['predicted_anomaly'].map({1: 0, -1: 1})

print("Training complete.")
print(f"Model saved as 'enhanced_model.pkl'")
print(f"Anomalies detected: {df['predicted_anomaly'].sum()} out of {len(df)}")
print("\nFeature importance (approximate via variance):")
for i, col in enumerate(feature_columns):
    print(f"  {col}: variance {X[:,i].var():.2f}")