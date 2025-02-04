class Graph:
    def __init__(self, graph):
        """Initialize an empty adjacency list."""
        self.adj_list = {}
        for node in graph.nodes:
            adj_list[node] = node.edges
        self.graph = graph

    def add_node(self, node):
        """Add a node to the graph."""
        if node not in self.adj_list:
            self.adj_list[node] = []

    def add_edge(self, node1, node2):
        """Add an edge between two nodes (undirected graph)."""
        if node1 not in self.adj_list:
            self.add_node(node1)
        if node2 not in self.adj_list:
            self.add_node(node2)
        self.adj_list[node1].append(node2)
        self.adj_list[node2].append(node1)

    def remove_edge(self, node1, node2):
        """Remove an edge between two nodes."""
        if node1 in self.adj_list and node2 in self.adj_list[node1]:
            self.adj_list[node1].remove(node2)
        if node2 in self.adj_list and node1 in self.adj_list[node2]:
            self.adj_list[node2].remove(node1)

    def remove_node(self, node):
        """Remove a node and its edges from the graph."""
        if node in self.adj_list:
            for neighbor in self.adj_list[node]:
                self.adj_list[neighbor].remove(node)
            del self.adj_list[node]

    def prune_leaves(self, iterations):
        """Recursively remove all nodes with degree 1."""
        
        for i in range(0, iterations):
            degree_map = {node: 0 for node in self.adj_list}
            for node in self.adj_list:
                for endpoint in self.adj_list[node]:
                    degree_map[endpoint] += 1
            leaves = [node for node in degree_map if degree_map[node] == 1]
            if not leaves:
                break
            for leaf in leaves:
                self.remove_node(leaf)

    def display(self):
        """Print the adjacency list of the graph."""
        for node, neighbors in self.adj_list.items():
            print(f"{node}: {neighbors}")
