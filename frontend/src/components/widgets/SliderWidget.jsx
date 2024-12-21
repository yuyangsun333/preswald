import React, { useState } from "react";

const SliderWidget = ({ label, min = 0, max = 100, defaultValue = 50 }) => {
  const [value, setValue] = useState(defaultValue);

  return (
    <div className="p-4 bg-white">
      <label className="block text-sm font-medium text-gray-900">
        {label}
      </label>
      <div className="mt-2">
        <input
          type="range"
          min={min}
          max={max}
          value={value}
          onChange={(e) => setValue(e.target.value)}
          className="w-full h-2 bg-gray-200 rounded-lg appearance-none focus:outline-none focus:ring-2 focus:ring-blue-500 focus:ring-offset-2"
        />
        <div className="flex justify-between mt-2 text-sm text-gray-500">
          <span>{min}</span>
          <span className="font-medium text-gray-900">{value}</span>
          <span>{max}</span>
        </div>
      </div>
    </div>
  );
};

export default SliderWidget;
