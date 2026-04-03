import pandas as pd
import numpy as np
from datetime import datetime, timedelta

def generate_sample_data():
    LAT_MIN, LAT_MAX = 24.0, 30.0
    LON_MIN, LON_MAX = -95.0, -80.0

    np.random.seed(42)
    num_vessels = 5
    timesteps = 100
    start_time = datetime(2025, 1, 1, 0, 0, 0)

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
            speed = 10 + np.random.normal(0, 2)
            course = np.degrees(np.arctan2(end_lat-start_lat, end_lon-start_lon)) + np.random.normal(0, 10)
            records.append({
                'timestamp': start_time + timedelta(minutes=10*t),
                'vessel_id': vessel_id,
                'lat': lat,
                'lon': lon,
                'speed': speed,
                'course': course,
                'sensor': 'AIS'
            })

    # Inject anomaly: vessel 3 high speed
    for t in range(50, 61):
        idx = t + (3-1)*timesteps
        records[idx]['speed'] = 25 + np.random.normal(0, 2)

    df = pd.DataFrame(records)
    df.to_csv('ais_data.csv', index=False)
    print("Sample AIS data saved to ais_data.csv")

if __name__ == '__main__':
    generate_sample_data()