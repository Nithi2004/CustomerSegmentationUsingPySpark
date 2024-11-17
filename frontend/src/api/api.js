import axios from "axios";

// Function to send input features to the Flask backend and get the prediction
export const predict = async (features) => {
  try {
    const response = await axios.post("http://127.0.0.1:5000/predict", {
      features,
    });
    return response.data; // Return the response containing the prediction
  } catch (error) {
    throw new Error("Failed to fetch prediction: " + error.message);
  }
};
