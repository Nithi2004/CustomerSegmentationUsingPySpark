import pickle
from flask import Flask, request, jsonify
from flask_cors import CORS  # To handle CORS issues

# Load the trained KMeans model
with open("kmeans_model.pkl", "rb") as file:
    model = pickle.load(file)

app = Flask(__name__)
CORS(app)  # Enable CORS for all routes

@app.route("/")
def home():
    return "Backend is running!"

@app.route("/predict", methods=["POST"])
def predict():
    data = request.json
    try:
        # Extract features from the input
        features = data.get("features", [])
        if not features or not isinstance(features, list):
            return jsonify({"error": "Invalid or missing features"}), 400
        
        # Perform prediction
        prediction = model.predict([features])[0]
        print(f"Prediction: {prediction}")  # Log the prediction
        
        # Map numeric prediction to a label (you can adjust this based on your model)
        label_map = {
            0: "Low-value customers",
            1: "High-value customers",
            2: "Frequent buyers",
            3: "New customers"
        }
        prediction_label = label_map.get(prediction, "Unknown cluster")
        
        return jsonify({"prediction": prediction_label})
    except Exception as e:
        return jsonify({"error": str(e)}), 500

if __name__ == "__main__":
    app.run(debug=True)
