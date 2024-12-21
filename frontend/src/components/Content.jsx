import React from "react";

const Content = ({ children }) => {
  return (
    <div className="flex-1 p-6 bg-gray-100 overflow-y-auto">
      {children}
    </div>
  );
};

export default Content;
