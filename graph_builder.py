import pandas as pd
import networkx as nx
import math
import pickle

def haversine(lat1, lon1, lat2, lon2):
    R = 6371
    phi1 = math.radians(lat1)
    phi2 = math.radians(lat2)
    delta_phi = math.radians(lat2 - lat1)
    delta_lambda = math.radians(lon2 - lon1)
    a = math.sin(delta_phi/2)**2 + math.cos(phi1)*math.cos(phi2)*math.sin(delta_lambda/2)**2
    c = 2 * math.atan2(math.sqrt(a), math.sqrt(1-a))
    return R * c

def build_graph_for_time(df, timestamp):
    G = nx.Graph()
    for _, row in df.iterrows():
        G.add_node(row['vessel_id'],
                   lat=row['lat'],
                   lon=row['lon'],
                   speed=row['speed'],
                   course=row['course'])
    vessels = list(df['vessel_id'])
    for i in range(len(vessels)):
        for j in range(i+1, len(vessels)):
            vi, vj = vessels[i], vessels[j]
            coord_i = (df[df['vessel_id']==vi].iloc[0]['lat'],
                       df[df['vessel_id']==vi].iloc[0]['lon'])
            coord_j = (df[df['vessel_id']==vj].iloc[0]['lat'],
                       df[df['vessel_id']==vj].iloc[0]['lon'])
            dist = haversine(coord_i[0], coord_i[1], coord_j[0], coord_j[1])
            if dist < 2.0:   # 2 km threshold
                G.add_edge(vi, vj, distance=dist)
    return G

def build_graphs_from_df(df):
    graphs = []
    for ts, group in df.groupby('timestamp'):
        G = build_graph_for_time(group, ts)
        graphs.append((ts, G))
    return graphs

def build_graphs_from_sample():
    df = pd.read_csv('fused_data.csv')
    df['timestamp'] = pd.to_datetime(df['timestamp'])
    graphs = build_graphs_from_df(df)
    with open('graphs.pkl', 'wb') as f:
        pickle.dump(graphs, f)
    print("Graphs saved to graphs.pkl")