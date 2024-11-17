import os
from flask import Flask, request, jsonify
from flask_cors import CORS
from pyspark.sql import SparkSession
from pyspark.ml.clustering import KMeansModel
from pyspark.ml.classification import LogisticRegressionModel
from pyspark.ml.feature import VectorAssembler, StandardScaler

# Initialize Flask app
app = Flask(__name__)
CORS(app)

# Initialize Spark session
spark = SparkSession.builder.appName('customer_segmentation_api').getOrCreate()

# Load saved models
unsupervised_model = KMeansModel.load("models/best_unsupervised_model")
supervised_model = LogisticRegressionModel.load("models/best_supervised_model")

# Define the prediction route
@app.route('/predict', methods=['POST'])
def predict():
    try:
        # Parse JSON input
        data = request.json
        recency = float(data['recency'])
        frequency = float(data['frequency'])
        monetary_value = float(data['monetary_value'])

        # Create a Spark DataFrame for the input
        input_data = [(recency, frequency, monetary_value)]
        input_df = spark.createDataFrame(input_data, ['recency', 'frequency', 'monetary_value'])

        # Assemble and scale features
        assembler = VectorAssembler(inputCols=['recency', 'frequency', 'monetary_value'], outputCol='features')
        input_df = assembler.transform(input_df)

        scaler = StandardScaler(inputCol='features', outputCol='scaled_features', withMean=False, withStd=True)
        scaler_model = scaler.fit(input_df)
        input_df = scaler_model.transform(input_df)

        # Unsupervised Prediction (KMeans)
        unsupervised_result = unsupervised_model.transform(input_df)
        cluster = unsupervised_result.select("prediction").collect()[0][0]

        # Supervised Prediction (Logistic Regression)
        supervised_result = supervised_model.transform(input_df)
        classification = supervised_result.select("prediction").collect()[0][0]

        # Return predictions
        return jsonify({
            "unsupervised_model": "KMeans",
            "cluster": int(cluster),
            "supervised_model": "LogisticRegression",
            "class": int(classification),
            "message": "Prediction successful."
        })

    except Exception as e:
        return jsonify({"error": str(e)})

if __name__ == '__main__':
    app.run(debug=True, port=5000)
