import React, { useState } from "react";
import axios from "axios";

function App() {
  const [formData, setFormData] = useState({
    recency: "",
    frequency: "",
    monetary_value: "",
  });

  const [result, setResult] = useState(null);

  const handleChange = (e) => {
    setFormData({ ...formData, [e.target.name]: e.target.value });
  };

  const handleSubmit = async (e) => {
    e.preventDefault();
    try {
      const response = await axios.post(
        "http://localhost:5000/predict",
        formData
      );
      setResult(response.data);
    } catch (error) {
      console.error("Error fetching predictions:", error);
    }
  };

  return (
    <div style={{ padding: "20px" }}>
      <h1>Customer Segmentation</h1>
      <form onSubmit={handleSubmit}>
        <div>
          <label>Recency (days): </label>
          <input
            type="number"
            name="recency"
            value={formData.recency}
            onChange={handleChange}
            required
          />
        </div>
        <div>
          <label>Frequency (number of purchases): </label>
          <input
            type="number"
            name="frequency"
            value={formData.frequency}
            onChange={handleChange}
            required
          />
        </div>
        <div>
          <label>Monetary Value ($): </label>
          <input
            type="number"
            name="monetary_value"
            value={formData.monetary_value}
            onChange={handleChange}
            required
          />
        </div>
        <button type="submit">Predict</button>
      </form>

      {result && (
        <div>
          <h2>Prediction Results</h2>
          <p>
            <strong>Unsupervised Model (KMeans)</strong>
          </p>
          <p>Predicted Cluster: {result.cluster}</p>
          <p>
            <strong>Supervised Model (Logistic Regression)</strong>
          </p>
          <p>Predicted Class: {result.class}</p>
        </div>
      )}
    </div>
  );
}

export default App;
