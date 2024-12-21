import React from "react";

const ProgressWidget = ({ label, value }) => {
  return (
    <div>
      <label>{label}</label>
      <progress max="100" value={value}></progress>
    </div>
  );
};

export default ProgressWidget;
