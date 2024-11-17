import pickle
from flask import Flask, request, jsonify
from flask_cors import CORS  # To handle CORS issues

# Load the trained KMeans model (although we won't be using it in this case)
with open("kmeans_model.pkl", "rb") as file:
    model = pickle.load(file)

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

if __name__ == "__main__":
    app.run(debug=True)
