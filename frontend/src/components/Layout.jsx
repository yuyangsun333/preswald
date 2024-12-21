import React from "react";
import Sidebar from "./Sidebar";
import TopBar from "./TopBar";
import Content from "./Content";

// Layout Component
const Layout = ({ children }) => {
  return (
    <div style={styles.layout}>
      <TopBar />
      <div style={styles.main}>
        <Sidebar />
        <Content>{children}</Content>
      </div>
    </div>
  );
};

// Styles for Layout
const styles = {
  layout: {
    display: "flex",
    flexDirection: "column",
    height: "100vh",
  },
  main: {
    display: "flex",
    flex: 1,
  },
};

export default Layout;
