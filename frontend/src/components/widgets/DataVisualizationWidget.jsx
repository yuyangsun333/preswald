import React from "react";
import Plot from "react-plotly.js";

const DataVisualizationWidget = ({ data }) => {
  return (
    <div>
      <h3>Data Visualization</h3>
      <Plot {...data} />
    </div>
  );
};

export default DataVisualizationWidget;
