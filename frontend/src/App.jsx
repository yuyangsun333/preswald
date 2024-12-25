import React, { useEffect, useState } from "react";

import DynamicComponents from "./components/DynamicComponents";
import Layout from "./components/Layout";
import { websocket } from "./utils/websocket";

const App = () => {
  const [components, setComponents] = useState([]);
  const [error, setError] = useState(null);
  const [config, setConfig] = useState(null);

  useEffect(() => {
    console.log("[App] Mounting, connecting to WebSocket");
    websocket.connect();

    const unsubscribe = websocket.subscribe((message) => {
      console.log("[App] Received WebSocket message:", message);
      
      if (message.type === "components") {
        console.log("[App] Updating components:", message.components);
        const updatedComponents = message.components.map(component => {
          if (component.id) {
            const currentState = websocket.getComponentState(component.id);
            console.log(`[App] Component ${component.id} state:`, {
              current: currentState,
              default: component.value
            });
            return {
              ...component,
              value: currentState !== undefined ? currentState : component.value
            };
          }
          return component;
        });
        setComponents(updatedComponents);
        setError(null);
      } 
      else if (message.type === "error") {
        console.error("[App] Received error:", message.content);
        setError(message.content.message);
      } 
      else if (message.type === "config") {
        console.log("[App] Received config:", message.config);
        setConfig(message.config);
      } 
      else if (message.type === "component_update") {
        console.log("[App] Received component update:", message);
        setComponents(prevComponents => {
          const updatedComponents = prevComponents.map(component => {
            if (component.id === message.component_id) {
              console.log(`[App] Updating component ${component.id}:`, {
                oldValue: component.value,
                newValue: message.value
              });
              return { ...component, value: message.value };
            }
            return component;
          });
          console.log("[App] Updated components after state change:", updatedComponents);
          return updatedComponents;
        });
      }
    });

    return () => {
      console.log("[App] Unmounting, cleaning up WebSocket");
      unsubscribe();
    };
  }, []);

  useEffect(() => {
    const updateTitle = () => {
      const title = config?.project?.title;
      if (title) {
        console.log("[App] Updating document title to:", title);
        document.title = title;
      }
    };

    updateTitle();

    document.addEventListener('visibilitychange', updateTitle);
    return () => document.removeEventListener('visibilitychange', updateTitle);
  }, [config]);

  const handleComponentUpdate = (componentId, value) => {
    console.log("[App] Component update:", {
      componentId,
      value,
      timestamp: new Date().toISOString()
    });
    
    // Update local state immediately
    setComponents(prevComponents => {
      const updatedComponents = prevComponents.map(component => {
        if (component.id === componentId) {
          console.log(`[App] Updating local component ${component.id}:`, {
            oldValue: component.value,
            newValue: value
          });
          return { ...component, value };
        }
        return component;
      });
      return updatedComponents;
    });
    
    // Send update to WebSocket
    websocket.updateComponentState(componentId, value);
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
