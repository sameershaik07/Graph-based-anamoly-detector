import pandas as pd
import numpy as np
from datetime import datetime, timedelta

np.random.seed(42)

def generate_enhanced_dataset(num_vessels=10, timesteps_per_vessel=50):
    records = []
    start_time = datetime(2025, 4, 1, 0, 0, 0)
    
    vessel_types = ['Cargo', 'Tanker', 'Fishing', 'Passenger', 'Container']
    type_speed_ranges = {
        'Cargo': (12, 20),
        'Tanker': (10, 18),
        'Fishing': (2, 8),
        'Passenger': (20, 30),
        'Container': (15, 25)
    }
    
    for v in range(1, num_vessels+1):
        vtype = np.random.choice(vessel_types)
        base_speed = np.random.uniform(*type_speed_ranges[vtype])
        base_course = np.random.uniform(0, 360)
        base_lat = np.random.uniform(25.0, 30.0)   # Gulf of Mexico region
        base_lon = np.random.uniform(-90.0, -85.0)
        
        # Simulate path with occasional anomalies
        for t in range(timesteps_per_vessel):
            timestamp = start_time + timedelta(minutes=5*t)
            
            # Determine if this record is anomalous (10% chance)
            is_anomaly = False
            if np.random.rand() < 0.1:
                is_anomaly = True
            
            # Normal behavior
            if not is_anomaly:
                speed = base_speed + np.random.normal(0, 1)
                course = base_course + np.random.normal(0, 5)
                accel = np.random.normal(0, 0.5)
                heading_rate = np.random.normal(0, 2)
                lat = base_lat + np.random.normal(0, 0.01) * (t/50)
                lon = base_lon + np.random.normal(0, 0.01) * (t/50)
                ais_gap = np.random.randint(10, 300)   # seconds
                dist_to_lane = np.random.uniform(0, 5)
                dist_to_port = np.random.uniform(10, 50)
            else:
                # Anomalous behavior - modify one or more parameters
                anomaly_type = np.random.choice(['speed_spike', 'sharp_turn', 'ais_off', 'off_lane', 'port_intrusion'])
                if anomaly_type == 'speed_spike':
                    speed = base_speed * np.random.uniform(2.5, 4)
                    accel = 10
                else:
                    speed = base_speed + np.random.normal(0, 1)
                
                if anomaly_type == 'sharp_turn':
                    course = (base_course + np.random.uniform(90, 180)) % 360
                    heading_rate = 45
                else:
                    course = base_course + np.random.normal(0, 5)
                
                if anomaly_type == 'ais_off':
                    ais_gap = 3600   # 1 hour gap
                else:
                    ais_gap = np.random.randint(10, 300)
                
                if anomaly_type == 'off_lane':
                    dist_to_lane = np.random.uniform(15, 30)
                else:
                    dist_to_lane = np.random.uniform(0, 5)
                
                if anomaly_type == 'port_intrusion':
                    dist_to_port = np.random.uniform(0, 2)
                else:
                    dist_to_port = np.random.uniform(10, 50)
                
                lat = base_lat + np.random.normal(0, 0.05) * (t/50)
                lon = base_lon + np.random.normal(0, 0.05) * (t/50)
                accel = np.random.normal(0, 0.5)
                heading_rate = np.random.normal(0, 2)
            
            # Clamp values
            speed = max(0, min(50, speed))
            course = course % 360
            accel = max(-10, min(10, accel))
            heading_rate = max(-30, min(30, heading_rate))
            
            records.append({
                'vessel_id': f'Vessel_{v}',
                'timestamp': timestamp,
                'lat': lat,
                'lon': lon,
                'speed': round(speed, 2),
                'course': round(course, 1),
                'vessel_type': vtype,
                'acceleration': round(accel, 2),
                'heading_rate': round(heading_rate, 1),
                'distance_to_shipping_lane_nm': round(dist_to_lane, 2),
                'distance_to_port_nm': round(dist_to_port, 2),
                'time_since_last_ais_sec': ais_gap,
                'is_anomaly': 1 if is_anomaly else 0
            })
    
    df = pd.DataFrame(records)
    return df

if __name__ == '__main__':
    df = generate_enhanced_dataset(num_vessels=15, timesteps_per_vessel=60)
    df.to_csv('enhanced_vessel_data.csv', index=False)
    print(f"✅ Generated {len(df)} records with {df['is_anomaly'].sum()} anomalies")
    print(df.head())