import React, { useState } from "react";
import { predict } from "../api/api";
import "./InputForm.css"; // Import the custom CSS file

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
      const features = [
        parseFloat(recency),
        parseInt(quantity),
        parseFloat(monetaryValue),
      ];
      // Send features to the backend for prediction
      const prediction = await predict(features);
      
      // Set the prediction result to display
      setResult(prediction.prediction);  // Get prediction string
    } catch (err) {
      setError(err.message);
    }
  };

  return (
    <div className="input-form-container">
      <h2 className="form-heading">Predict Customer Segmentation</h2>
      <form onSubmit={handleSubmit} className="form">
        <div className="form-field">
          <label htmlFor="recency" className="label">
            Recency (days):
          </label>
          <input
            type="number"
            id="recency"
            value={recency}
            onChange={(e) => setRecency(e.target.value)}
            className="input"
            required
          />
        </div>

        <div className="form-field">
          <label htmlFor="quantity" className="label">
            Quantity:
          </label>
          <input
            type="number"
            id="quantity"
            value={quantity}
            onChange={(e) => setQuantity(e.target.value)}
            className="input"
            required
          />
        </div>

        <div className="form-field">
          <label htmlFor="monetaryValue" className="label">
            Monetary Value:
          </label>
          <input
            type="number"
            id="monetaryValue"
            value={monetaryValue}
            onChange={(e) => setMonetaryValue(e.target.value)}
            className="input"
            required
          />
        </div>

        <button type="submit" className="submit-button">
          Predict
        </button>
      </form>

      {result && (
        <div className="result-message">{`Cluster Prediction: ${result}`}</div>
      )}

      {error && <div className="error-message">{`Error: ${error}`}</div>}
    </div>
  );
};

export default InputForm;
