import React from "react";

const Sidebar = () => {
  return (
    <div className="w-64 bg-gray-800 text-white h-full p-4 shadow-lg">
      <ul className="space-y-4">
        <li><a href="#" className="hover:text-gray-400">Home</a></li>
        <li><a href="#" className="hover:text-gray-400">Settings</a></li>
        <li><a href="#" className="hover:text-gray-400">Profile</a></li>
      </ul>
    </div>
  );
};

export default Sidebar;
