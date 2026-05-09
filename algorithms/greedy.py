import heapq

def greedy(graph, start, goal):
    """
    Greedy Best-First Search — always expands the node closest to goal by heuristic.
    NOTE: Does not guarantee least-cost or shortest path.
    Returns (path, cost) or (None, None) if no path found.
    """

    if start not in graph.edges or goal not in graph.edges:
        return None, None

    # (h_cost, current_node, path_so_far, cost_so_far)
    queue = [(graph.get_heuristic(start), start, [start], 0)]
    visited = set()

    while queue:
        _, node, path, cost = heapq.heappop(queue)

        if node == goal:
            return path, cost

        if node in visited:
            continue
        visited.add(node)

        for neighbor, weight in graph.get_neighbors(node):
            if neighbor not in visited:
                h = graph.get_heuristic(neighbor)  # defaults to 0 if not set
                heapq.heappush(queue, (h, neighbor, path + [neighbor], cost + weight))

    return None, None