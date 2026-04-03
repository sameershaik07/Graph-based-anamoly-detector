import numpy as np
import pickle
import networkx as nx

def extract_node_features(graph):
    features = []
    node_ids = []
    for node, data in graph.nodes(data=True):
        # Basic features: speed, course, lat, lon
        vec = [data['speed'], data['course'], data['lat'], data['lon']]
        # Add degree (number of neighbours)
        vec.append(graph.degree(node))
        # Add average distance to neighbours (if any)
        if graph.degree(node) > 0:
            avg_dist = np.mean([graph.edges[node, nb]['distance'] for nb in graph.neighbors(node)])
            vec.append(avg_dist)
        else:
            vec.append(0)
        features.append(vec)
        node_ids.append(node)
    return np.array(features), node_ids

# Load graphs
with open('graphs.pkl', 'rb') as f:
    graphs = pickle.load(f)

# Collect all feature vectors (one per node per time)
all_features = []
all_labels = []   # we'll label anomalies later

for ts, G in graphs:
    feats, nodes = extract_node_features(G)
    all_features.append(feats)
    # For now, we don't have ground truth labels, but we'll simulate some anomalies.
    # For training, we'll use only normal windows.

# Let's split: first 80% of timesteps for training (normal only)
train_end = int(0.8 * len(all_features))
train_features = np.vstack(all_features[:train_end])
test_features = np.vstack(all_features[train_end:])

# Normalise features (important for autoencoder)
from sklearn.preprocessing import StandardScaler
scaler = StandardScaler()
train_features_norm = scaler.fit_transform(train_features)
test_features_norm = scaler.transform(test_features)

# Save preprocessed features
np.save('train_features.npy', train_features_norm)
np.save('test_features.npy', test_features_norm)