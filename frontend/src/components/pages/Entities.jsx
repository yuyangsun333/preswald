import ReactFlow, {
  MiniMap,
  Controls,
  Background,
} from "reactflow";
import "reactflow/dist/style.css";

const Entities = () => {
  // Toggle demo data (set to true to use demo data)
  const useDemoData = false;

  // Example extracted entities and relationships (used only if `useDemoData` is true)
  const demoEntities = [
    { id: "orders", name: "Orders", attributes: ["Order ID", "Customer ID", "Amount"] },
    { id: "customers", name: "Customers", attributes: ["Customer ID", "Name", "Email"] },
    { id: "products", name: "Products", attributes: ["Product ID", "Name", "Price"] },
  ];

  const demoRelationships = [
    { source: "orders", target: "customers", label: "Customer ID" },
    { source: "orders", target: "products", label: "Product ID" },
  ];

  // Conditionally load data based on `useDemoData`
  const entities = useDemoData ? demoEntities : [];
  const relationships = useDemoData ? demoRelationships : [];

  // Generate nodes from entities
  const nodes = entities.map((entity, index) => ({
    id: entity.id,
    position: { x: index * 250, y: 100 },
    data: {
      label: (
        <div className="bg-white shadow-md p-4 rounded-md border">
          <h3 className="font-bold text-lg">{entity.name}</h3>
          <ul className="mt-2 text-sm text-gray-600">
            {entity.attributes.map((attr, idx) => (
              <li key={idx}>• {attr}</li>
            ))}
          </ul>
        </div>
      ),
    },
    style: {
      width: 200,
      borderRadius: 8,
      padding: 10,
    },
  }));

  // Generate edges from relationships
  const edges = relationships.map((rel, index) => ({
    id: `edge-${index}`,
    source: rel.source,
    target: rel.target,
    label: rel.label,
    markerEnd: { type: "arrowclosed" },
    style: { stroke: "#4A5568" },
    labelStyle: { fill: "#4A5568", fontSize: 12 },
  }));

  return (
    <div className="h-screen">
      <h1 className="text-2xl font-bold p-4">Entities</h1>
      {entities.length > 0 ? (
        <ReactFlow
          nodes={nodes}
          edges={edges}
          fitView
          fitViewOptions={{ padding: 0.2 }}
        >
          <MiniMap
            nodeStrokeColor={(n) => (n.type === "input" ? "#0041d0" : "#ff0072")}
            nodeColor={(n) => (n.type === "input" ? "#0041d0" : "#fff")}
            nodeBorderRadius={2}
          />
          <Controls />
          <Background />
        </ReactFlow>
      ) : (
        <p className="text-center text-gray-500 p-6">
          No entities available. Add real data to display the entity diagram.
        </p>
      )}
    </div>
  );
};

export default Entities;
