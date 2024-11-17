import React from "react";
import InputForm from "../components/InputForm";
import "./Home.css"; // Import custom CSS file

const Home = () => {
  return (
    <div className="home-container">
      <div className="content">
        <h1 className="main-heading">Customer Segmentation</h1>
        <InputForm />
      </div>
    </div>
  );
};

export default Home;
