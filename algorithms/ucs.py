import heapq

def ucs(graph, start, goal):
    """
    Uniform Cost Search — expands the least-cost node first.
    Guarantees the optimal (lowest cost) path.
    Equivalent to A* with h(n) = 0, or Dijkstra's algorithm.
    Returns (path, cost) or (None, None) if no path found.
    """

    if start not in graph.edges or goal not in graph.edges:
        return None, None

    # (cost_so_far, current_node, path_so_far)
    queue = [(0, start, [start])]
    visited = set()

    while queue:
        cost, node, path = heapq.heappop(queue)

        if node == goal:
            return path, cost

        if node in visited:
            continue
        visited.add(node)

        for neighbor, weight in graph.get_neighbors(node):
            if neighbor not in visited:  # ✅ skip already visited nodes
                heapq.heappush(queue, (cost + weight, neighbor, path + [neighbor]))

    return None, None