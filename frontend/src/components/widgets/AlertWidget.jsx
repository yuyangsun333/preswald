import React from "react";
import { ExclamationTriangleIcon } from "@heroicons/react/20/solid";

const levelStyles = {
  success: {
    background: "bg-green-50",
    text: "text-green-800",
    icon: "text-green-400",
    description: "text-green-700",
  },
  warning: {
    background: "bg-yellow-50",
    text: "text-yellow-800",
    icon: "text-yellow-400",
    description: "text-yellow-700",
  },
  error: {
    background: "bg-red-50",
    text: "text-red-800",
    icon: "text-red-400",
    description: "text-red-700",
  },
  info: {
    background: "bg-blue-50",
    text: "text-blue-800",
    icon: "text-blue-400",
    description: "text-blue-700",
  },
};

const AlertWidget = ({ message, level = "info" }) => {
  const styles = levelStyles[level] || levelStyles.info;

  return (
    <div className={`rounded-md p-4 ${styles.background}`}>
      <div className="flex">
        <div className="shrink-0">
          <ExclamationTriangleIcon
            aria-hidden="true"
            className={`size-5 ${styles.icon}`}
          />
        </div>
        <div className="ml-3">
          <h3 className={`text-sm font-medium ${styles.text}`}>Attention Needed</h3>
          <div className={`mt-2 text-sm ${styles.description}`}>
            <p>{message}</p>
          </div>
        </div>
      </div>
    </div>
  );
};

export default AlertWidget;
