import React from "react";

const Content = ({ children }) => {
  return <div style={styles.content}>{children}</div>;
};

// Styles for Content
const styles = {
  content: {
    flex: 1,
    padding: "20px",
    overflowY: "auto",
  },
};

export default Content;
