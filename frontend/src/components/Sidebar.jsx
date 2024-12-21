import React from "react";

const Sidebar = () => {
  return (
    <div style={styles.sidebar}>
      <ul>
        <li><a href="#">Home</a></li>
        <li><a href="#">Settings</a></li>
        <li><a href="#">Profile</a></li>
      </ul>
    </div>
  );
};

// Styles for Sidebar
const styles = {
  sidebar: {
    width: "250px",
    backgroundColor: "#1e293b",
    color: "white",
    padding: "20px",
    boxShadow: "2px 0 4px rgba(0, 0, 0, 0.1)",
  },
};

export default Sidebar;
