import React from "react";

const AlertWidget = ({ message, level }) => {
  return <div className={`alert alert-${level}`}>{message}</div>;
};

export default AlertWidget;
