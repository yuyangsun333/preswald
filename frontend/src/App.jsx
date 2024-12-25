import React, { useEffect, useState } from "react";

import DynamicComponents from "./components/DynamicComponents";
import Layout from "./components/Layout";
import { websocket } from "./utils/websocket";

const App = () => {
  const [components, setComponents] = useState([]);
  const [error, setError] = useState(null);
  const [config, setConfig] = useState(null);
  const [isConnected, setIsConnected] = useState(false);

  useEffect(() => {
    // Connect to WebSocket
    websocket.connect();

    // Subscribe to WebSocket messages
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
              value: currentState !== undefined ? currentState : component.value,
              error: null
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
        
        // Update component error state if component-specific error
        if (message.content.componentId) {
          setComponents(prevComponents => 
            prevComponents.map(component => 
              component.id === message.content.componentId 
                ? { ...component, error: message.content.message }
                : component
            )
          );
        }
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
              return { 
                ...component, 
                value: message.value,
                error: null // Clear any previous errors
              };
            }
            return component;
          });
          console.log("[App] Updated components after state change:", updatedComponents);
          return updatedComponents;
        });
      }
      else if (message.type === "connection_status") {
        setIsConnected(message.connected);
        if (!message.connected) {
          setError("Lost connection to server. Attempting to reconnect...");
        } else {
          setError(null);
        }
      }
    });

    // Cleanup on unmount
    return () => {
      unsubscribe();
      websocket.disconnect();
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
          return { 
            ...component, 
            value,
            error: null // Clear any previous errors
          };
        }
        return component;
      });
      return updatedComponents;
    });
    
    // Send update to WebSocket
    try {
      websocket.updateComponentState(componentId, value);
    } catch (error) {
      console.error("[App] Error updating component state:", error);
      setComponents(prevComponents => 
        prevComponents.map(component => 
          component.id === componentId 
            ? { ...component, error: error.message }
            : component
        )
      );
    }
  };

  if (!isConnected) {
    return (
      <Layout>
        <div className="flex items-center justify-center h-screen">
          <div className="text-center">
            <div className="animate-spin rounded-full h-12 w-12 border-b-2 border-blue-600 mx-auto mb-4"></div>
            <p className="text-gray-600">Connecting to server...</p>
          </div>
        </div>
      </Layout>
    );
  }

  if (error && !components.length) {
    return (
      <Layout>
        <div className="p-4 bg-red-50 border border-red-300 rounded-md">
          <p className="text-red-700">{error}</p>
        </div>
      </Layout>
    );
  }

  return (
    <Layout>
      {error && (
        <div className="p-4 mb-4 bg-red-50 border border-red-300 rounded-md">
          <p className="text-red-700">{error}</p>
        </div>
      )}
      {components.length === 0 ? (
        <div className="flex items-center justify-center h-64">
          <div className="text-center">
            <div className="animate-spin rounded-full h-8 w-8 border-b-2 border-blue-600 mx-auto mb-4"></div>
            <p className="text-gray-600">Loading components...</p>
          </div>
        </div>
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
