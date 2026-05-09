import heapq

def astar(graph, start, goal):
    """
    A* Search — finds the lowest-cost path using f(n) = g(n) + h(n).
    Returns (path, cost) or (None, None) if no path found.
    """

    # f_cost, g_cost, current_node, path_so_far
    queue = [(graph.get_heuristic(start), 0, start, [start])]
    visited = set()

    while queue:
        f, g, node, path = heapq.heappop(queue)

        if node == goal:
            return path, g

        if node in visited:
            continue
        visited.add(node)

        for neighbor, weight in graph.get_neighbors(node):
            if neighbor not in visited:
                new_g = g + weight
                h = graph.get_heuristic(neighbor)  # defaults to 0 if not set
                new_f = new_g + h
                heapq.heappush(queue, (new_f, new_g, neighbor, path + [neighbor]))

    return None, None