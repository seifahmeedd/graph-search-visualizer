from collections import deque

def bfs(graph, start, goal):
    """
    Breadth-First Search — finds the shallowest (fewest hops) path.
    NOTE: Does not guarantee least-cost path, only least number of edges.
    Returns (path, cost) or (None, None) if no path found.
    """

    if start not in graph.edges or goal not in graph.edges:
        return None, None

    # (current_node, path_so_far, cost_so_far)
    queue = deque([(start, [start], 0)])
    visited = set()

    while queue:
        node, path, cost = queue.popleft()

        if node == goal:
            return path, cost

        if node in visited:
            continue
        visited.add(node)

        for neighbor, weight in graph.get_neighbors(node):
            if neighbor not in visited:
                queue.append((neighbor, path + [neighbor], cost + weight))

    return None, None