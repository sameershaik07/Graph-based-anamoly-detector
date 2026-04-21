# Graph-Based Anomaly Detector for Maritime Domain Awareness

![GitHub last commit](https://img.shields.io/github/last-commit/sameershaik07/Graph-based-anamoly-detector?style=for-the-badge)
![GitHub repo size](https://img.shields.io/github/repo-size/sameershaik07/Graph-based-anamoly-detector?style=for-the-badge)
![GitHub language count](https://img.shields.io/github/languages/count/sameershaik07/Graph-based-anamoly-detector?style=for-the-badge)
![GitHub top language](https://img.shields.io/github/languages/top/sameershaik07/Graph-based-anamoly-detector?style=for-the-badge)

## 🚀 Project Overview

This project implements a **Graph-Based Anomaly Detection System** designed for **Maritime Domain Awareness (MDA)**. It leverages **Multi-Modal Sensor Fusion** and **Machine Learning** to identify suspicious vessel behaviors, such as illegal fishing, smuggling, or piracy, by analyzing vessel interaction patterns.

The system aims to provide an automated and intelligent solution to enhance maritime security and surveillance, moving beyond traditional rule-based methods to a more adaptive and data-driven approach.

## ✨ Features

-   **Multi-Modal Sensor Fusion**: Integrates data from various sources (e.g., AIS, radar, satellite) to create a comprehensive view of maritime activity.
-   **Vessel Interaction Graph Construction**: Builds dynamic graphs where nodes represent vessels and edges signify interactions or proximity, capturing complex relationships.
-   **Machine Learning for Anomaly Detection**: Applies advanced ML algorithms to the constructed graphs to detect unusual patterns and flag potential anomalies.
-   **Anomaly Scoring**: Assigns risk scores to vessels or interactions, indicating the likelihood of suspicious activity.
-   **Web-Based Monitoring Dashboard**: Provides a user-friendly interface for real-time visualization of vessel movements, alerts, and anomaly insights.
-   **Data Preprocessing & Management**: Includes modules for cleaning, transforming, and managing diverse maritime datasets.

## 🛠️ Technologies Used

-   **Python**: Core programming language.
-   **Flask**: Web framework for building the monitoring dashboard and API.
-   **Pandas & NumPy**: For data manipulation and numerical operations.
-   **Scikit-learn (or similar)**: For machine learning model training and anomaly detection.
-   **NetworkX (or similar)**: For graph construction and analysis.
-   **HTML/CSS/JavaScript**: For the front-end of the web application.
-   **Pickle**: For model serialization.

## ⚙️ Installation

To set up the project locally, follow these steps:

1.  **Clone the repository:**
    ```bash
    git clone https://github.com/sameershaik07/Graph-based-anamoly-detector.git
    cd Graph-based-anamoly-detector
    ```

2.  **Create a virtual environment (recommended):**
    ```bash
    python -m venv venv
    source venv/bin/activate  # On Windows use `venv\Scripts\activate`
    ```

3.  **Install dependencies:**
    ```bash
    pip install -r requirements.txt
    ```
    *(Note: A `requirements.txt` file is assumed. If not present, you may need to install `flask`, `pandas`, `numpy`, `scikit-learn`, `networkx` manually.)*

4.  **Prepare data and models:**
    The project includes scripts like `data_generator.py`, `preprocess.py`, `graph_builder.py`, and `train_model.py` (or their `enhanced_` versions). You might need to run these to generate necessary data files (`fused_data.csv`, `graphs.pkl`) and trained models (`enhanced_model.pkl`, `feature_names.pkl`).
    
    For initial setup, you can run:
    ```bash
    python data_generator.py
    python preprocess.py
    python graph_builder.py
    python train_model.py
    # Or use the enhanced versions if available and preferred
    python enhanced_data_generator.py
    python enhanced_train_model.py
    ```

## 🚀 Usage

1.  **Run the Flask application:**
    ```bash
    python app.py
    ```

2.  **Access the dashboard:**
    Open your web browser and navigate to `http://127.0.0.1:5000/` (or the port specified by Flask).

3.  **Login:**
    Use the default credentials (if any are set in `app.py`, e.g., `admin`/`password123`) to access the monitoring dashboard.

4.  **Monitor and Detect Anomalies:**
    The dashboard will display vessel movements and highlight detected anomalies based on the processed data and trained models.

## 📂 Project Structure

```
Graph-based-anamoly-detector/
├── __pycache__/             # Python cache files
├── templates/               # HTML templates for Flask app
├── uploads/                 # Directory for uploaded files
├── ais_data.csv             # Sample AIS data
├── app.py                   # Main Flask application
├── data_generator.py        # Script to generate sample data
├── enhanced_anomaly_scorer.py # Enhanced anomaly scoring logic
├── enhanced_data_generator.py # Enhanced data generation script
├── enhanced_model.pkl       # Trained anomaly detection model
├── enhanced_train_model.py  # Script to train enhanced model
├── enhanced_vessel_data.csv # Enhanced vessel data
├── feature_names.pkl        # Feature names for the model
├── features.py              # Feature engineering logic
├── fused_data.csv           # Fused multi-modal data
├── generate_test_data.py    # Script to generate test data
├── graph_builder.py         # Script to build vessel interaction graphs
├── graphs.pkl               # Serialized graph data
├── preprocess.py            # Data preprocessing script
├── test_vessels.csv         # Test vessel data
└── train_model.py           # Script to train the initial model
```

## 🤝 Contributing

Contributions are welcome! If you have suggestions for improvements or new features, please open an issue or submit a pull request.

