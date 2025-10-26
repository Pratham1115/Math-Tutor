import os
import joblib
import numpy as np

# Absolute paths
BASE_DIR = os.path.dirname(os.path.abspath(__file__))
model_path = os.path.join(BASE_DIR, "difficulty_model.pkl")
scaler_path = os.path.join(BASE_DIR, "scaler.pkl")

# Load model and scaler
model = joblib.load(model_path)
scaler = joblib.load(scaler_path)

# ✅ Function to predict next difficulty level
def predict_next_level(response_time, accuracy, hints, current_difficulty):
    # Prepare features
    features = np.array([[response_time, accuracy, hints, current_difficulty]])
    features_scaled = scaler.transform(features)
    
    # Predict next difficulty level
    prediction = model.predict(features_scaled)
    return prediction[0]
