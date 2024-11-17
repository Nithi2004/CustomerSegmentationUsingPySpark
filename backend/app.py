from flask import Flask, request, jsonify
from pyspark.sql import SparkSession
from pyspark.ml.clustering import KMeansModel
import pickle
import pandas as pd

# Initialize Spark and Flask
spark = SparkSession.builder.appName("CustomerSegmentationAPI").getOrCreate()
app = Flask(__name__)

# Load models
best_unsupervised_model = KMeansModel.load("best_unsupervised_model")
with open("best_supervised_model.pkl", "rb") as f:
    best_supervised_model = pickle.load(f)

@app.route("/predict", methods=["POST"])
def predict():
    data = request.json
    features = pd.DataFrame([data])
    prediction = best_supervised_model.predict(features)[0]
    spark_df = spark.createDataFrame(features)
    vector_assembler = VectorAssembler(inputCols=["recency", "frequency", "monetary_value"], outputCol="features")
    vectorized_data = vector_assembler.transform(spark_df)
    cluster = best_unsupervised_model.transform(vectorized_data).select("prediction").collect()[0][0]

    return jsonify({
        "supervised_prediction": int(prediction),
        "unsupervised_cluster": int(cluster),
        "model_accuracy": best_supervised_acc
    })

if __name__ == "__main__":
    app.run(debug=True)
