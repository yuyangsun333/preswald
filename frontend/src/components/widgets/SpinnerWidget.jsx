import React from "react";

const SpinnerWidget = ({ label }) => {
  return (
    <div>
      <label>{label}</label>
      <div className="spinner">Loading...</div>
    </div>
  );
};

export default SpinnerWidget;
