import numpy as np
from sklearn.ensemble import IsolationForest

train_features = np.load('train_features.npy')
test_features = np.load('test_features.npy')

# Train Isolation Forest
clf = IsolationForest(contamination=0.05, random_state=42)
clf.fit(train_features)

# Predict anomalies (-1 = anomaly)
pred = clf.predict(test_features)
anomaly_flags = (pred == -1)

print(f"Anomalies found: {np.sum(anomaly_flags)} / {len(test_features)}")