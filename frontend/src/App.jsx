import React, { useEffect, useState } from "react";
import Layout from "./components/Layout";

const App = () => {
  const [components, setComponents] = useState([]);
  const [loading, setLoading] = useState(true);

  useEffect(() => {
    const fetchComponents = async () => {
      try {
        const response = await fetch("/api/components");
        const data = await response.json();
        setComponents(data);
      } catch (error) {
        console.error("Error fetching components:", error);
      } finally {
        setLoading(false);
      }
    };

    fetchComponents();
  }, []);

  if (loading) {
    return <div>Loading...</div>;
  }

  return (
    <Layout>
      <h2>Dynamic Components</h2>
      <div>
        {components.map((component, index) => {
          switch (component.type) {
            case "button":
              return (
                <button key={index} onClick={() => alert("Button clicked!")}>
                  {component.label}
                </button>
              );
            case "slider":
              return (
                <div key={index}>
                  <label>{component.label}</label>
                  <input type="range" min={component.min} max={component.max} />
                </div>
              );
            default:
              return <div key={index}>Unknown component type</div>;
          }
        })}
      </div>
    </Layout>
  );
};

export default App;
