import React, { useEffect, useState } from "react";
import { BrowserRouter as Router, Routes, Route } from "react-router-dom";

import Layout from "./components/Layout";
import { websocket } from "./utils/websocket";

import Dashboard from "./components/pages/Dashboard";
import Connections from "./components/pages/Connections"; 
import Metrics from "./components/pages/Metrics";
import Entities from "./components/pages/Entities";

const App = () => {
  const [components, setComponents] = useState([]);
  const [error, setError] = useState(null);
  const [config, setConfig] = useState(null);
  const [isConnected, setIsConnected] = useState(false);

  useEffect(() => {
    // Connect to WebSocket and handle messages
    websocket.connect();

    const unsubscribe = websocket.subscribe((message) => {
      handleWebSocketMessage(message);
    });

    return () => {
      unsubscribe();
      websocket.disconnect();
    };
  }, []);

  useEffect(() => {
    // Update document title based on config
    const updateTitle = () => {
      const title = config?.project?.title;
      if (title) {
        document.title = title;
      }
    };

    updateTitle();

    document.addEventListener("visibilitychange", updateTitle);
    return () => document.removeEventListener("visibilitychange", updateTitle);
  }, [config]);

  const handleWebSocketMessage = (message) => {
    console.log("[App] Received WebSocket message:", message);

    if (message.type === "components") {
      updateComponents(message.components);
    } else if (message.type === "error") {
      handleError(message.content);
    } else if (message.type === "config") {
      setConfig(message.config);
    } else if (message.type === "component_update") {
      updateComponentState(message);
    } else if (message.type === "connection_status") {
      setIsConnected(message.connected);
      if (!message.connected) setError("Lost connection to server. Attempting to reconnect...");
      else setError(null);
    }
  };

  const updateComponents = (components) => {
    const updatedComponents = components.map((component) => {
      if (component.id) {
        const currentState = websocket.getComponentState(component.id);
        return {
          ...component,
          value: currentState !== undefined ? currentState : component.value,
          error: null,
        };
      }
      return component;
    });
    setComponents(updatedComponents);
    setError(null);
  };

  const handleError = (errorContent) => {
    console.error("[App] Received error:", errorContent);
    setError(errorContent.message);

    if (errorContent.componentId) {
      setComponents((prevComponents) =>
        prevComponents.map((component) =>
          component.id === errorContent.componentId
            ? { ...component, error: errorContent.message }
            : component
        )
      );
    }
  };

  const updateComponentState = (message) => {
    setComponents((prevComponents) =>
      prevComponents.map((component) =>
        component.id === message.component_id
          ? { ...component, value: message.value, error: null }
          : component
      )
    );
  };

  const handleComponentUpdate = (componentId, value) => {
    try {
      websocket.updateComponentState(componentId, value);
    } catch (error) {
      console.error("[App] Error updating component state:", error);
      setComponents((prevComponents) =>
        prevComponents.map((component) =>
          component.id === componentId ? { ...component, error: error.message } : component
        )
      );
    }
  };

  return (
    <Router>
      <Layout>
        {!isConnected ? (
          <div className="flex items-center justify-center h-screen">
            <div className="text-center">
              <div className="animate-spin rounded-full h-12 w-12 border-b-2 border-blue-600 mx-auto mb-4"></div>
              <p className="text-gray-600">Connecting to server...</p>
            </div>
          </div>
        ) : (
          <Routes>
            <Route
              path="/"
              element={
                <Dashboard
                  components={components}
                  error={error}
                  handleComponentUpdate={handleComponentUpdate}
                />
              }
            />
            <Route path="/connections" element={<Connections />} />
            <Route path="/metrics" element={<Metrics />} />
            <Route path="/entities" element={<Entities />} />
          </Routes>
        )}
      </Layout>
    </Router>
  );
};

export default App;
