import React from "react";

const SelectboxWidget = ({ label, options, defaultOption }) => {
  return (
    <div>
      <label>
        {label}
        <select defaultValue={defaultOption}>
          {options.map((option, index) => (
            <option key={index} value={option}>
              {option}
            </option>
          ))}
        </select>
      </label>
    </div>
  );
};

export default SelectboxWidget;
