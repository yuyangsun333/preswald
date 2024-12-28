import React from "react";
import DynamicComponents from "../DynamicComponents";

const Dashboard = ({ components, error, handleComponentUpdate }) => {
  return (
    <div>
      {error && (
        <div className="p-4 mb-4 bg-red-50 border border-red-300 rounded-md">
          <p className="text-red-700">{error}</p>
        </div>
      )}
      {components.length === 0 ? (
        <div className="flex items-center justify-center h-64">
          <div className="text-center">
            <div className="animate-spin rounded-full h-8 w-8 border-b-2 border-blue-600 mx-auto mb-4"></div>
            <p className="text-gray-600">Loading components...</p>
          </div>
        </div>
      ) : (
        <DynamicComponents components={components} onComponentUpdate={handleComponentUpdate} />
      )}
    </div>
  );
};

export default Dashboard;
