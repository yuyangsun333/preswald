import React from "react";
import Plot from "react-plotly.js";

const DataVisualizationWidget = ({ data }) => {
  // Fallback sample data for the chart
  const sampleData = {
    data: [
      {
        x: ["Category A", "Category B", "Category C"],
        y: [10, 15, 20],
        type: "bar",
        marker: { color: "blue" },
      },
    ],
    layout: {
      title: "Sample Bar Chart",
      xaxis: { title: "Categories" },
      yaxis: { title: "Values" },
    },
    config: {
      responsive: true,
    },
  };

  return (
    <div>
      <h3 className="text-lg font-semibold text-gray-900 mb-4">Data Visualization</h3>
      <Plot {...(data || sampleData)} />
    </div>
  );
};

export default DataVisualizationWidget;
