import pandas as pd
import numpy as np

def preprocess_sample_data():
    ais = pd.read_csv('ais_data.csv')
    ais['timestamp'] = pd.to_datetime(ais['timestamp'])

    # Simulate radar and satellite data (just for fusion example)
    radar = ais.copy()
    radar['sensor'] = 'RADAR'
    radar['speed'] = radar['speed'] + np.random.normal(0, 0.5)
    radar = radar.sample(frac=0.9)

    satellite = ais.sample(frac=0.3)
    satellite['sensor'] = 'SAT'
    satellite['speed'] = satellite['speed'] + np.random.normal(0, 0.2)

    all_data = pd.concat([ais, radar, satellite], ignore_index=True)
    all_data.sort_values(['vessel_id', 'timestamp'], inplace=True)

    fused = all_data.groupby(['vessel_id', 'timestamp'], as_index=False).agg({
        'lat': 'median',
        'lon': 'median',
        'speed': 'median',
        'course': 'median'
    })

    fused.to_csv('fused_data.csv', index=False)
    print("Fused data saved to fused_data.csv")

if __name__ == '__main__':
    preprocess_sample_data()