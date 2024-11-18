import React, { useState } from "react";
import "./InputForm.css"; // Import the custom CSS file

const InputForm = () => {
  const [recency, setRecency] = useState("");
  const [quantity, setQuantity] = useState("");
  const [monetaryValue, setMonetaryValue] = useState("");
  const [result, setResult] = useState(null);

  // Logic for determining the cluster based on the input
  const determineCluster = (recency, quantity, monetaryValue) => {
    if (monetaryValue > 100000 && quantity > 50) {
      return "High-value frequent buyer";
    } else if (monetaryValue > 100000) {
      return "High-value customer";
    } else if (quantity > 50) {
      return "Frequent buyer";
    } else if (recency < 30 && quantity > 10) {
      return "Active customer";
    } else if (monetaryValue > 50000) {
      return "High spender";
    } else if (recency < 30) {
      return "New customer";
    } else if (monetaryValue < 1000) {
      return "Low-value customer";
    } else {
      return "Other";
    }
  };

  const handleSubmit = (e) => {
    e.preventDefault();
    setResult(null);

    // Ensure inputs are valid before processing
    if (!recency || !quantity || !monetaryValue) {
      setResult("Error: Please fill in all fields correctly.");
      return;
    }

    const cluster = determineCluster(
      parseFloat(recency),
      parseInt(quantity),
      parseFloat(monetaryValue)
    );

    setResult(cluster);
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
    </div>
  );
};

export default InputForm;
