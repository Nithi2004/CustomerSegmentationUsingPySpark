import React, { useState } from "react";
import { predict } from "../api/api";

const InputForm = () => {
  const [recency, setRecency] = useState("");
  const [quantity, setQuantity] = useState("");
  const [monetaryValue, setMonetaryValue] = useState("");
  const [result, setResult] = useState(null);
  const [error, setError] = useState("");

  const handleSubmit = async (e) => {
    e.preventDefault();
    setError("");
    setResult(null);

    try {
      const features = [parseFloat(recency), parseInt(quantity), parseFloat(monetaryValue)];
      const prediction = await predict(features);
      setResult(prediction);
    } catch (err) {
      setError(err.message);
    }
  };

  return (
    <div>
      <h2>Predict Customer Segmentation</h2>
      <form onSubmit={handleSubmit}>
        <div>
          <label>Recency (days):</label>
          <input
            type="number"
            value={recency}
            onChange={(e) => setRecency(e.target.value)}
            required
          />
        </div>
        <div>
          <label>Quantity:</label>
          <input
            type="number"
            value={quantity}
            onChange={(e) => setQuantity(e.target.value)}
            required
          />
        </div>
        <div>
          <label>Monetary Value:</label>
          <input
            type="number"
            value={monetaryValue}
            onChange={(e) => setMonetaryValue(e.target.value)}
            required
          />
        </div>
        <button type="submit">Predict</button>
      </form>
      {result && <div>Cluster Prediction: {result}</div>}
      {error && <div style={{ color: "red" }}>Error: {error}</div>}
    </div>
  );
};

export default InputForm;
