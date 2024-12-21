import React, { useEffect, useState } from "react";
import Layout from "./components/Layout";
import DynamicComponents from "./components/DynamicComponents";

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
      <DynamicComponents components={components} />
    </Layout>
  );
};

export default App;
