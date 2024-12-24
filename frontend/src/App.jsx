import React, { useEffect, useState } from "react";

import DynamicComponents from "./components/DynamicComponents";
import Layout from "./components/Layout";
import { websocket } from "./utils/websocket";

const App = () => {
  const [components, setComponents] = useState([]);
  const [error, setError] = useState(null);
  const [config, setConfig] = useState(null);

  useEffect(() => {
    console.log("App mounted, connecting to WebSocket");
    websocket.connect();

    const unsubscribe = websocket.subscribe((message) => {
      console.log("Received WebSocket message:", message);
      if (message.type === "components") {
        console.log("Updating components:", message.components);
        setComponents(message.components);
        setError(null);
      } else if (message.type === "error") {
        console.error("Received error:", message.content);
        setError(message.content.message);
      } else if (message.type === "config") {
        console.log("Received config:", message.config);
        setConfig(message.config);
      }
    });

    return () => {
      console.log("App unmounting, cleaning up WebSocket");
      unsubscribe();
    };
  }, []);

  useEffect(() => {
    const updateTitle = () => {
      const title = config?.project?.title;
      if (title) {
        console.log("Updating document title to:", title);
        document.title = title;
      }
    };

    updateTitle();

    document.addEventListener('visibilitychange', updateTitle);
    return () => document.removeEventListener('visibilitychange', updateTitle);
  }, [config]);

  const handleComponentUpdate = (componentId, value) => {
    console.log("Component update:", componentId, value);
    websocket.sendMessage({
      type: "component_update",
      componentId,
      value
    });
  };

  if (error) {
    return (
      <Layout>
        <div className="text-red-600 p-4">
          Error: {error}
        </div>
      </Layout>
    );
  }

  return (
    <Layout>
      {components.length === 0 ? (
        <div className="p-4">Loading components...</div>
      ) : (
        <DynamicComponents 
          components={components}
          onComponentUpdate={handleComponentUpdate}
        />
      )}
    </Layout>
  );
};

export default App;
