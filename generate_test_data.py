import pandas as pd
import numpy as np
from datetime import datetime, timedelta

def generate_test_csv(filename='test_vessels.csv'):
    # Maritime region (Gulf of Mexico)
    LAT_MIN, LAT_MAX = 24.0, 30.0
    LON_MIN, LON_MAX = -95.0, -80.0

    np.random.seed(123)
    num_vessels = 5
    timesteps = 100
    start_time = datetime(2025, 3, 25, 0, 0, 0)

    records = []
    for vessel_id in range(1, num_vessels+1):
        start_lat = np.random.uniform(LAT_MIN, LAT_MAX)
        start_lon = np.random.uniform(LON_MIN, LON_MAX)
        end_lat = np.random.uniform(LAT_MIN, LAT_MAX)
        end_lon = np.random.uniform(LON_MIN, LON_MAX)

        for t in range(timesteps):
            alpha = t / timesteps
            lat = start_lat + alpha * (end_lat - start_lat) + np.random.normal(0, 0.05)
            lon = start_lon + alpha * (end_lon - start_lon) + np.random.normal(0, 0.05)
            speed = 8 + np.random.normal(0, 1)   # normal speed ~8 knots
            course = np.degrees(np.arctan2(end_lat-start_lat, end_lon-start_lon)) + np.random.normal(0, 5)
            records.append({
                'timestamp': start_time + timedelta(minutes=10*t),
                'vessel_id': vessel_id,
                'lat': lat,
                'lon': lon,
                'speed': speed,
                'course': course,
                'sensor': 'AIS'
            })

    # ===== ANOMALIES (last until the end) =====
    # Vessel 2: high speed from t=50 to end
    for t in range(50, timesteps):
        idx = t + (2-1)*timesteps
        records[idx]['speed'] = 28 + np.random.normal(0, 2)

    # Vessel 4: high speed + course change from t=60 to end
    for t in range(60, timesteps):
        idx = t + (4-1)*timesteps
        records[idx]['speed'] = 22 + np.random.normal(0, 1.5)
        records[idx]['course'] = 45 + np.random.normal(0, 10)

    # Vessel 5: position offset + very high speed from t=70 to end
    for t in range(70, timesteps):
        idx = t + (5-1)*timesteps
        records[idx]['lat'] += 2.5
        records[idx]['lon'] += 3.0
        records[idx]['speed'] = 28 + np.random.normal(0, 1)  # boosted to 28

    df = pd.DataFrame(records)
    df.to_csv(filename, index=False)
    print(f"Test data saved to {filename}")

if __name__ == '__main__':
    generate_test_csv()