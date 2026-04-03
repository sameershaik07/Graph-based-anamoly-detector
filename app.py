import os
import pickle
import pandas as pd
import numpy as np
from flask import Flask, render_template, request, redirect, url_for, session, jsonify
from werkzeug.utils import secure_filename

app = Flask(__name__)
app.secret_key = 'your-secret-key-change-this'
app.config['UPLOAD_FOLDER'] = 'uploads'
app.config['ALLOWED_EXTENSIONS'] = {'csv'}

os.makedirs(app.config['UPLOAD_FOLDER'], exist_ok=True)

USERS = {'admin': 'password123'}

def allowed_file(filename):
    return '.' in filename and filename.rsplit('.', 1)[1].lower() in app.config['ALLOWED_EXTENSIONS']

# ------------------- Sample data generation (if missing) -------------------
def ensure_sample_data():
    """Generate sample data if no fused_data.csv or graphs.pkl exist."""
    if os.path.exists('fused_data.csv') and os.path.exists('graphs.pkl'):
        return True

    try:
        from data_generator import generate_sample_data
        from preprocess import preprocess_sample_data
        from graph_builder import build_graphs_from_sample

        print("No data found. Generating sample data...")
        generate_sample_data()
        preprocess_sample_data()
        build_graphs_from_sample()
        return True
    except Exception as e:
        print(f"Error generating sample data: {e}")
        return False

# ------------------- Routes -------------------
@app.route('/')
def home():
    if 'username' in session:
        return redirect(url_for('dashboard'))
    return redirect(url_for('login'))

@app.route('/login', methods=['GET', 'POST'])
def login():
    if request.method == 'POST':
        username = request.form['username']
        password = request.form['password']
        if username in USERS and USERS[username] == password:
            session['username'] = username
            return redirect(url_for('dashboard'))
        else:
            return render_template('login.html', error='Invalid credentials')
    return render_template('login.html')

@app.route('/logout')
def logout():
    session.pop('username', None)
    return redirect(url_for('login'))

@app.route('/upload', methods=['GET', 'POST'])
def upload_page():
    if 'username' not in session:
        return redirect(url_for('login'))

    if request.method == 'POST':
        if 'file' not in request.files:
            return render_template('upload.html', error='No file part')
        file = request.files['file']
        if file.filename == '':
            return render_template('upload.html', error='No file selected')
        if file and allowed_file(file.filename):
            filename = secure_filename(file.filename)
            filepath = os.path.join(app.config['UPLOAD_FOLDER'], filename)
            file.save(filepath)

            try:
                df = pd.read_csv(filepath)
                df['timestamp'] = pd.to_datetime(df['timestamp'])
                df.to_csv('fused_data.csv', index=False)

                from graph_builder import build_graphs_from_df
                graphs = build_graphs_from_df(df)
                with open('graphs.pkl', 'wb') as f:
                    pickle.dump(graphs, f)

                return redirect(url_for('dashboard'))
            except Exception as e:
                return render_template('upload.html', error=f'Error processing file: {str(e)}')
        else:
            return render_template('upload.html', error='Allowed file type: CSV')

    return render_template('upload.html')

@app.route('/dashboard')
def dashboard():
    if 'username' not in session:
        return redirect(url_for('login'))

    if not os.path.exists('graphs.pkl') or not os.path.exists('fused_data.csv'):
        if not ensure_sample_data():
            return "No data available. Please upload a CSV file or run the data generation scripts.", 404

    return render_template('map.html')

@app.route('/map_data')
def map_data():
    if 'username' not in session:
        return jsonify([])

    try:
        with open('graphs.pkl', 'rb') as f:
            graphs = pickle.load(f)

        if not graphs:
            print("No graphs loaded")
            return jsonify([])

        # Get the most recent graph
        latest_ts, latest_graph = graphs[-1]
        print(f"Loaded {len(graphs)} graphs, latest has {latest_graph.number_of_nodes()} nodes")

        markers = []
        for node, data in latest_graph.nodes(data=True):
            lat = data.get('lat')
            lon = data.get('lon')
            speed = data.get('speed', 0)

            # Skip if lat/lon missing
            if lat is None or lon is None:
                continue

            # Simple anomaly score based on speed
            anomaly_score = max(0, (speed - 15) / 15)
            anomaly_score = min(1, anomaly_score)
            is_anomaly = anomaly_score > 0.3

            markers.append({
                'lat': lat,
                'lon': lon,
                'vessel_id': node,
                'speed': speed,
                'anomaly_score': anomaly_score,
                'anomaly': is_anomaly
            })

        print(f"Returning {len(markers)} markers")
        return jsonify(markers)

    except Exception as e:
        print("Error loading graphs:", e)
        return jsonify([])

if __name__ == '__main__':
    app.run(debug=True)