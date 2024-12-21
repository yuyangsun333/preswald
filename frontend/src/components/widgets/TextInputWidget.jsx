import React from "react";

const TextInputWidget = ({ label, placeholder }) => {
  return (
    <div>
      <label>
        {label}
        <input type="text" placeholder={placeholder} />
      </label>
    </div>
  );
};

export default TextInputWidget;
