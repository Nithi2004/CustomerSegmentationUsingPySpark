import pickle
from flask import Flask, request, jsonify
from flask_cors import CORS  # To handle CORS issues
import logging
import os

# Set up logging for debugging
logging.basicConfig(level=logging.INFO)

# Get the absolute path of the current directory
current_dir = os.path.dirname(os.path.abspath(__file__))

# Load the trained KMeans model (using absolute path)
model_path = os.path.join(current_dir, "kmeans_model.pkl")
logging.info(f"Loading model from {model_path}")
try:
    with open(model_path, "rb") as file:
        model = pickle.load(file)
    logging.info("Model loaded successfully!")
except FileNotFoundError:
    logging.error(f"Model file not found at {model_path}")
    raise

# Initialize Flask app
app = Flask(__name__)
CORS(app)  # Enable CORS for all routes

@app.route("/")
def home():
    return "Backend is running!"

# Custom classification logic based on recency, quantity, and monetary value
def classify_customer(recency, quantity, monetary_value):
    # Priority logic based on Quantity and Monetary Value
    if monetary_value > 100000 and quantity > 50:
        return "High-value frequent buyer"
    elif monetary_value > 100000:
        return "High-value customer"
    elif quantity > 50:
        return "Frequent buyer"
    elif recency < 30 and quantity > 10:
        return "Active customer"
    elif monetary_value > 50000:
        return "High spender"
    elif recency < 30:
        return "New customer"
    elif monetary_value < 1000:
        return "Low-value customer"
    else:
        return "Other"

@app.route("/predict", methods=["POST"])
def predict():
    data = request.json
    try:
        # Extract features from the input
        features = data.get("features", [])
        if not features or len(features) != 3:
            return jsonify({"error": "Invalid or missing features"}), 400

        recency, quantity, monetary_value = features

        # Apply custom classification logic
        prediction_label = classify_customer(recency, quantity, monetary_value)

        return jsonify({"prediction": prediction_label})
    except Exception as e:
        return jsonify({"error": str(e)}), 500

# Run the app on Render's provided port
if __name__ == "__main__":
    port = int(os.environ.get("PORT", 5000))
    app.run(host="0.0.0.0", port=port, debug=True)
