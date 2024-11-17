import pickle
from flask import Flask, request, jsonify
from flask_cors import CORS  # To handle CORS issues

# Load the trained KMeans model
with open("best_kmeans_model.pkl", "rb") as file:
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
        prediction = model.predict([features])
        return jsonify({"prediction": prediction.tolist()})
    except Exception as e:
        return jsonify({"error": str(e)}), 500
import pickle

with open("best_kmeans_model.pkl", "rb") as file:
    obj = pickle.load(file)

print(type(obj))  # Should print <class 'sklearn.cluster._kmeans.KMeans'>

if __name__ == "__main__":
    app.run(debug=True)
