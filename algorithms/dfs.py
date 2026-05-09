def dfs(graph, start, goal):
    """
    Depth-First Search — explores as deep as possible before backtracking.
    NOTE: Does not guarantee shortest or least-cost path.
    Returns (path, cost) or (None, None) if no path found.
    """

    if start not in graph.edges or goal not in graph.edges:
        return None, None

    # (current_node, path_so_far, cost_so_far)
    stack = [(start, [start], 0)]
    visited = set()

    while stack:
        node, path, cost = stack.pop()

        if node == goal:
            return path, cost

        if node in visited:
            continue
        visited.add(node)

        for neighbor, weight in graph.get_neighbors(node):
            if neighbor not in visited:
                stack.append((neighbor, path + [neighbor], cost + weight))

    return None, None