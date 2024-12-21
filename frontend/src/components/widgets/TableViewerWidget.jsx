import React from "react";

const TableViewerWidget = ({ data }) => {
  if (!data || data.length === 0) {
    return (
      <div className="p-4 bg-white ">
        <p className="text-sm font-medium text-gray-500">No data available</p>
      </div>
    );
  }

  return (
    <div className="p-4 bg-white  overflow-x-auto">
      <h3 className="text-lg font-medium text-gray-900 mb-4">Table Viewer</h3>
      <table className="min-w-full table-auto border-collapse border border-gray-300">
        <thead className="bg-gray-50">
          <tr>
            {Object.keys(data[0]).map((key) => (
              <th
                key={key}
                className="px-4 py-2 text-left text-sm font-medium text-gray-900 border border-gray-300"
              >
                {key}
              </th>
            ))}
          </tr>
        </thead>
        <tbody>
          {data.map((row, index) => (
            <tr
              key={index}
              className={index % 2 === 0 ? "bg-white" : "bg-gray-50"}
            >
              {Object.values(row).map((value, idx) => (
                <td
                  key={idx}
                  className="px-4 py-2 text-sm text-gray-700 border border-gray-300"
                >
                  {value !== null && value !== undefined ? value : "N/A"}
                </td>
              ))}
            </tr>
          ))}
        </tbody>
      </table>
    </div>
  );
};

export default TableViewerWidget;
