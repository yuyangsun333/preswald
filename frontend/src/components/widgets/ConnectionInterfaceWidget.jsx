import React, { useState } from "react";

const ConnectionInterfaceWidget = () => {
  const [source, setSource] = useState("");
  const [type, setType] = useState("csv");

  const handleConnect = () => {
    alert(`Connecting to ${source} as ${type}`);
  };

  return (
    <div>
      <h3>Connection Interface</h3>
      <label>
        Source:
        <input
          type="text"
          value={source}
          onChange={(e) => setSource(e.target.value)}
          placeholder="Enter data source"
        />
      </label>
      <label>
        Type:
        <select value={type} onChange={(e) => setType(e.target.value)}>
          <option value="csv">CSV</option>
          <option value="json">JSON</option>
          <option value="parquet">Parquet</option>
          <option value="postgres">Postgres</option>
        </select>
      </label>
      <button onClick={handleConnect}>Connect</button>
    </div>
  );
};

export default ConnectionInterfaceWidget;
