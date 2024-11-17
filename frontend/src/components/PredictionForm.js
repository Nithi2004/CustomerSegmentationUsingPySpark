import React, { useState } from "react";
import axios from "axios";

function PredictionForm() {
  const [recency, setRecency] = useState("");
  const [quantity, setQuantity] = useState("");
  const [monetaryValue, setMonetaryValue] = useState("");
  const [prediction, setPrediction] = useState(null);

  const handleSubmit = async (e) => {
    e.preventDefault();
    try {
      const response = await axios.post("http://localhost:5000/predict", {
        recency: parseFloat(recency),
        Quantity: parseFloat(quantity),
        monetary_value: parseFloat(monetaryValue),
      });
      setPrediction(response.data.segment);
      alert(`${response.data.model}`);
    } catch (error) {
      console.error("Error fetching prediction", error);
    }
  };

  return (
    <div>
      <form onSubmit={handleSubmit}>
        <input
          type="number"
          placeholder="Recency"
          value={recency}
          onChange={(e) => setRecency(e.target.value)}
        />
        <input
          type="number"
          placeholder="Quantity"
          value={quantity}
          onChange={(e) => setQuantity(e.target.value)}
        />
        <input
          type="number"
          placeholder="Monetary Value"
          value={monetaryValue}
          onChange={(e) => setMonetaryValue(e.target.value)}
        />
        <button type="submit">Predict Segment</button>
      </form>
      {prediction !== null && <div>Predicted Segment: {prediction}</div>}
    </div>
  );
}

export default PredictionForm;
