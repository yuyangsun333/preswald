import React from "react";

const TopBar = () => {
  return (
    <div className="flex items-center bg-blue-500 text-white px-4 py-2 shadow-md">
      <img src="/logo.png" alt="Logo" className="h-10 mr-2" />
      <h1 className="text-lg font-bold">Preswald App</h1>
    </div>
  );
};

export default TopBar;
