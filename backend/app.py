import os
from flask import Flask, request, jsonify
from flask_cors import CORS
import joblib
import numpy as np

# Initialize Flask app
app = Flask(__name__)
CORS(app)

# Load saved models (using joblib)
unsupervised_model = joblib.load("models/best_unsupervised_model.pkl")  # Assuming the unsupervised model is saved as .pkl
supervised_model = joblib.load("models/best_supervised_model.pkl")  # Assuming the supervised model is saved as .pkl

# Define the prediction route
@app.route('/predict', methods=['POST'])
def predict():
    try:
        # Parse JSON input
        data = request.json
        recency = float(data['recency'])
        frequency = float(data['frequency'])
        monetary_value = float(data['monetary_value'])

        # Prepare the input features for prediction
        input_data = np.array([[recency, frequency, monetary_value]])

        # Unsupervised Prediction (e.g., KMeans)
        cluster = unsupervised_model.predict(input_data)  # Get the predicted cluster from the unsupervised model

        # Supervised Prediction (e.g., Logistic Regression)
        classification = supervised_model.predict(input_data)  # Get the predicted class from the supervised model

        # Return predictions as JSON response
        return jsonify({
            "unsupervised_model": "KMeans",
            "cluster": int(cluster[0]),
            "supervised_model": "LogisticRegression",
            "class": int(classification[0]),
            "message": "Prediction successful."
        })

    except Exception as e:
        return jsonify({"error": str(e)})

if __name__ == '__main__':
    app.run(debug=True, port=5000)
