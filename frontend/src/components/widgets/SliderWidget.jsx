import React, { useState } from "react";

const SliderWidget = ({ label, min, max, defaultValue }) => {
  const [value, setValue] = useState(defaultValue);

  return (
    <div>
      <label>
        {label} ({value})
        <input
          type="range"
          min={min}
          max={max}
          value={value}
          onChange={(e) => setValue(e.target.value)}
        />
      </label>
    </div>
  );
};

export default SliderWidget;
