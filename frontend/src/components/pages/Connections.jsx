import React from "react";

const Connections = () => {
  // Toggle this variable to enable/disable dummy data
  const useDummyData = false;

  const connections = useDummyData
    ? [
        {
          id: 1,
          icon: "https://via.placeholder.com/40", // Replace with actual icon URL
          title: "User 1 - example_connection",
          description: "Connected by User 1",
          date: "October 21, 2024",
          status: "Connected",
        },
        {
          id: 2,
          icon: "https://via.placeholder.com/40", // Replace with actual icon URL
          title: "User 2 - another_connection",
          description: "Connected by User 2",
          date: "October 21, 2024",
          status: "Connected",
        },
      ]
    : [];

  return (
    <div className="p-5 max-w-4xl">
      <h1 className="text-2xl font-bold mb-4">Connections</h1>
      {connections.length === 0 ? (
        <p className="text-gray-500">No connections available.</p>
      ) : (
        <div className="space-y-4">
          {connections.map((connection) => (
            <div
              key={connection.id}
              className="flex items-center p-4 border rounded-lg shadow-sm hover:shadow-md transition-shadow"
            >
              {/* Icon */}
              <img
                src={connection.icon}
                alt="icon"
                className="w-10 h-10 rounded-full mr-4"
              />

              {/* Details */}
              <div className="flex-1">
                <h2 className="text-lg font-medium">{connection.title}</h2>
                <p className="text-sm text-gray-500">
                  {connection.date} • {connection.description}
                </p>
              </div>

              {/* Status */}
              <div className="flex items-center space-x-2">
                <span className="px-3 py-1 text-sm font-semibold text-green-800 bg-green-100 rounded-lg">
                  {connection.status}
                </span>
                <button
                  className="text-gray-400 hover:text-gray-600"
                  aria-label="Options"
                >
                  <svg
                    xmlns="http://www.w3.org/2000/svg"
                    className="h-5 w-5"
                    viewBox="0 0 20 20"
                    fill="currentColor"
                  >
                    <path d="M6 10a1 1 0 011-1h6a1 1 0 010 2H7a1 1 0 01-1-1z" />
                  </svg>
                </button>
              </div>
            </div>
          ))}
        </div>
      )}
    </div>
  );
};

export default Connections;
