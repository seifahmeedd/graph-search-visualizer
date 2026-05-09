class Graph:
    def __init__(self):
        self.edges = {}       # {node: [(neighbor, weight), ...]}
        self.heuristics = {}  # {node: h_value}

    def add_edge(self, node1, node2, weight=1):
        if node1 not in self.edges:
            self.edges[node1] = []
        if node2 not in self.edges:
            self.edges[node2] = []
        self.edges[node1].append((node2, weight))
        self.edges[node2].append((node1, weight))  # undirected graph

    def add_heuristic(self, node, value):
        self.heuristics[node] = value

    def get_neighbors(self, node):
        """Returns list of (neighbor, weight) for a given node. Safe — returns [] if node not found."""
        return self.edges.get(node, [])

    def get_heuristic(self, node):
        """Returns heuristic value for a node. Defaults to 0 if not set."""
        return self.heuristics.get(node, 0)