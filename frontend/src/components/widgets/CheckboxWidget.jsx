import React, { useState } from "react";

const CheckboxWidget = ({ label, defaultChecked }) => {
  const [checked, setChecked] = useState(defaultChecked);

  return (
    <div>
      <label>
        <input
          type="checkbox"
          checked={checked}
          onChange={() => setChecked(!checked)}
        />
        {label}
      </label>
    </div>
  );
};

export default CheckboxWidget;
