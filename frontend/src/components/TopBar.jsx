import React from "react";

const TopBar = () => {
  return (
    <div style={styles.topBar}>
      <img src="/logo.png" alt="Logo" style={styles.logo} />
      <h1 style={styles.title}>Preswald App</h1>
    </div>
  );
};

// Styles for TopBar
const styles = {
  topBar: {
    display: "flex",
    alignItems: "center",
    backgroundColor: "#3b82f6",
    color: "white",
    padding: "10px 20px",
    boxShadow: "0 2px 4px rgba(0, 0, 0, 0.1)",
  },
  logo: {
    height: "40px",
    marginRight: "10px",
  },
  title: {
    fontSize: "24px",
    margin: 0,
  },
};

export default TopBar;
