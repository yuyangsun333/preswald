import networkx as nx


class StateManager:
    def __init__(self):
        # Core data structures
        self.graph = nx.DiGraph()  # Stores function dependencies
        self.cache = {}  # Stores function results
        self.data_to_node = {}  # Maps data objects to their source nodes
        self.current_execution = None  # Tracks currently executing function

    def track_function_call(self, func, args, kwargs):
        print("tracking function call ", str(func))
        node_id = self._create_node_id(func, args, kwargs)
        print("tracking function call ", node_id)

        # Add node to graph if it doesn't exist
        if node_id not in self.graph:
            self.graph.add_node(node_id, func=func, args=args, kwargs=kwargs)

        # Track dependencies from two sources:

        # 1. Current execution context
        if self.current_execution:
            self.graph.add_edge(self.current_execution, node_id)

        # 2. Data object dependencies
        for arg in args:
            if arg in self.data_to_node:
                parent_node = self.data_to_node[arg]
                self.graph.add_edge(parent_node, node_id)

        for arg in kwargs.values():
            if arg in self.data_to_node:
                parent_node = self.data_to_node[arg]
                self.graph.add_edge(parent_node, node_id)

        return node_id

    def _create_node_id(self, func, args, kwargs):
        """Create a unique identifier for a function call"""
        # For now, a simple combination of function name and argument IDs
        arg_ids = [str(id(arg)) for arg in args]
        kwarg_ids = [f"{k}:{id(v)}" for k, v in kwargs.items()]
        return f"{func.__name__}_{'-'.join(arg_ids + kwarg_ids)}"

    def get_or_compute(self, node_id):
        """Get cached result or compute if necessary"""
        if node_id in self.cache:
            return self.cache[node_id]

        return self.execute(node_id)

    def execute(self, node_id):
        """Execute a function and cache its result"""
        # Set up execution context
        previous_execution = self.current_execution
        self.current_execution = node_id

        print("executing node ", node_id)

        try:
            # Get function and arguments
            node = self.graph.nodes[node_id]
            func = node["func"]
            args = node["args"]
            kwargs = node["kwargs"]

            # Execute function
            result = func(*args, **kwargs)

            # Cache result and track its source
            self.cache[node_id] = result
            self.data_to_node[result] = node_id

            return result
        finally:
            # Restore previous execution context
            self.current_execution = previous_execution

    def invalidate(self, node_id):
        """Invalidate a node and its descendants"""
        # Get all nodes that depend on this one
        descendants = nx.descendants(self.graph, node_id)
        affected_nodes = {node_id} | descendants

        # Remove them from cache
        for node in affected_nodes:
            self.cache.pop(node, None)
