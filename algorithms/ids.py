def dls(graph, node, goal, depth, path, cost):
    """
    Depth-Limited Search — recursive DFS with a depth cap.
    Returns (path, cost) if goal found, or (None, None) if not.
    """
    if node == goal:
        return path, cost

    if depth == 0:
        return None, None

    for neighbor, weight in graph.get_neighbors(node):
        if neighbor not in path:  # avoid cycles
            result_path, result_cost = dls(
                graph, neighbor, goal,
                depth - 1,
                path + [neighbor],
                cost + weight
            )
            if result_path:
                return result_path, result_cost

    return None, None


def ids(graph, start, goal):
    """
    Iterative Deepening Search — runs DLS with increasing depth limits.
    Guarantees shallowest path like BFS but uses much less memory.
    Returns (path, cost) or (None, None) if no path found.
    """

    if start not in graph.edges or goal not in graph.edges:
        return None, None

    max_depth = len(graph.edges)  # dynamic limit based on graph size

    for depth in range(max_depth + 1):
        path, cost = dls(graph, start, goal, depth, [start], 0)
        if path:
            return path, cost

    return None, None