import React from "react";

const SliderWidget = ({ label, min = 0, max = 100, value = 50, id, onChange }) => {
  const [localValue, setLocalValue] = React.useState(value);

  const handleChange = (e) => {
    const newValue = parseInt(e.target.value, 10);
    setLocalValue(newValue);
  };

  const handleMouseUp = () => {
    if (localValue !== value) {
      console.log("[SliderWidget] Change event:", {
        id,
        value: localValue,
        timestamp: new Date().toISOString()
      });
      onChange?.(localValue);
    }
  };

  React.useEffect(() => {
    setLocalValue(value);
  }, [value]);

  return (
    <div className="p-4 bg-white">
      <label htmlFor={id} className="block text-sm font-medium text-gray-900">
        {label}
      </label>
      <div className="mt-2">
        <input
          id={id}
          name={id}
          type="range"
          min={min}
          max={max}
          value={localValue}
          onChange={handleChange}
          onMouseUp={handleMouseUp}
          onTouchEnd={handleMouseUp}
          className="w-full h-2 bg-gray-200 rounded-lg appearance-none focus:outline-none focus:ring-2 focus:ring-blue-500 focus:ring-offset-2"
        />
        <div className="flex justify-between mt-2 text-sm text-gray-500">
          <span>{min}</span>
          <span className="font-medium text-gray-900">{localValue}</span>
          <span>{max}</span>
        </div>
      </div>
    </div>
  );
};

export default SliderWidget;
