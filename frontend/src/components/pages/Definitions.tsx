import React from "react";

const Definitions = () => {
  // Toggle this to enable/disable the definitions
  const showDefinitions = false;

  const definitions = showDefinitions
    ? [
        {
          id: 1,
          name: "Customer",
          description: "Represents a customer entity in the system.",
          type: "Entity",
          createdBy: "John Doe",
          dateCreated: "October 1, 2024",
          tags: ["CRM", "User Data"],
        },
        {
          id: 2,
          name: "Order",
          description: "Tracks customer orders, status, and delivery.",
          type: "Entity",
          createdBy: "Jane Smith",
          dateCreated: "October 5, 2024",
          tags: ["E-Commerce", "Sales"],
        },
        {
          id: 3,
          name: "Revenue",
          description: "Aggregates total revenue across products and regions.",
          type: "Metric",
          createdBy: "Alice Johnson",
          dateCreated: "October 10, 2024",
          tags: ["Finance", "KPIs"],
        },
      ]
    : [];

  return (
    <div className="p-5 max-w-7xl mx-auto">
      <h1 className="text-2xl font-bold mb-4">Definitions</h1>

      {definitions.length === 0 ? (
        <p className="text-gray-500">No definitions available.</p>
      ) : (
        <div className="space-y-4">
          {definitions.map((definition) => (
            <div
              key={definition.id}
              className="flex flex-col sm:flex-row items-start sm:items-center justify-between p-4 border rounded-lg shadow-sm hover:shadow-md transition-shadow"
            >
              {/* Name and Description */}
              <div className="flex-1">
                <h2 className="text-lg font-medium">{definition.name}</h2>
                <p className="text-sm text-gray-500">{definition.description}</p>
              </div>

              {/* Metadata */}
              <div className="text-sm text-gray-600 mt-2 sm:mt-0 sm:ml-4">
                <p>
                  <span className="font-semibold">Type:</span> {definition.type}
                </p>
                <p>
                  <span className="font-semibold">Created By:</span>{" "}
                  {definition.createdBy}
                </p>
                <p>
                  <span className="font-semibold">Date Created:</span>{" "}
                  {definition.dateCreated}
                </p>
                {definition.tags && (
                  <div className="mt-2">
                    <span className="font-semibold">Tags:</span>{" "}
                    {definition.tags.map((tag, index) => (
                      <span
                        key={index}
                        className="inline-block bg-blue-100 text-blue-800 text-xs font-medium mr-2 px-2.5 py-0.5 rounded"
                      >
                        {tag}
                      </span>
                    ))}
                  </div>
                )}
              </div>

              {/* Actions */}
              <div className="flex items-center space-x-2 mt-2 sm:mt-0">
                <button className="px-3 py-1 text-white bg-blue-500 rounded hover:bg-blue-600 text-sm">
                  View
                </button>
                <button className="px-3 py-1 text-white bg-red-500 rounded hover:bg-red-600 text-sm">
                  Delete
                </button>
              </div>
            </div>
          ))}
        </div>
      )}
    </div>
  );
};

export default Definitions;
