import React, { useState } from "react";

const ConnectionInterfaceWidget = () => {
  const [source, setSource] = useState("");
  const [type, setType] = useState("csv");

  const handleConnect = () => {
    alert(`Connecting to ${source} as ${type}`);
  };

  return (
    <div className="p-6 bg-white">
      <h3 className="text-lg font-semibold text-gray-900 mb-4">Connection Interface</h3>
      <div className="space-y-4">
        {/* Source Input */}
        <div>
          <label
            htmlFor="source"
            className="block text-sm font-medium text-gray-700"
          >
            Data Source
          </label>
          <input
            id="source"
            type="text"
            value={source}
            onChange={(e) => setSource(e.target.value)}
            placeholder="Enter data source"
            className="mt-1 block w-full rounded-md border-gray-300 shadow-sm focus:border-blue-500 focus:ring-blue-500 sm:text-sm"
          />
        </div>

        {/* Type Select */}
        <div>
          <label
            htmlFor="type"
            className="block text-sm font-medium text-gray-700"
          >
            Connection Type
          </label>
          <select
            id="type"
            value={type}
            onChange={(e) => setType(e.target.value)}
            className="mt-1 block w-full rounded-md border-gray-300 bg-white shadow-sm focus:border-blue-500 focus:ring-blue-500 sm:text-sm"
          >
            <option value="csv">CSV</option>
            <option value="json">JSON</option>
            <option value="parquet">Parquet</option>
            <option value="postgres">Postgres</option>
          </select>
        </div>

        {/* Connect Button */}
        <div>
          <button
            onClick={handleConnect}
            className="w-full rounded-md bg-blue-600 px-4 py-2 text-sm font-semibold text-white shadow-sm hover:bg-blue-700 focus-visible:outline focus-visible:outline-2 focus-visible:outline-offset-2 focus-visible:outline-blue-600"
          >
            Connect
          </button>
        </div>
      </div>
    </div>
  );
};

export default ConnectionInterfaceWidget;
