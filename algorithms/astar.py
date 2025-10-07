"""
astar.py - A* search on the model grid that respects TerrainTile.movement_cost
and treats Obstacle agents as impassable.
Returns a list of positions [(x,y), ...] including start and goal, or None if no path.
"""
import heapq

def _get_terrain_cost(model, pos):
    # Find any TerrainTile in the cell and return its movement_cost
    cell = model.grid.get_cell_list_contents(pos)
    for a in cell:
        # terrain tile class name
        if a.__class__.__name__ == "TerrainTile":
            return getattr(a, "movement_cost", 1.0)
    return 1.0

def _is_blocked(model, pos):
    # if any Obstacle exists in the cell or cell is out of bounds -> blocked
    x, y = pos
    if x < 0 or y < 0 or x >= model.width or y >= model.height:
        return True
    cell = model.grid.get_cell_list_contents(pos)
    for a in cell:
        if a.__class__.__name__ == "Obstacle":
            return True
    return False

def _neighbors(model, pos):
    # 4-neighborhood (up, down, left, right)
    x, y = pos
    candidates = [(x+1,y),(x-1,y),(x,y+1),(x,y-1)]
    valid = [c for c in candidates if 0 <= c[0] < model.width and 0 <= c[1] < model.height and not _is_blocked(model, c)]
    return valid

def heuristic(a, b):
    # Manhattan heuristic
    return abs(a[0]-b[0]) + abs(a[1]-b[1])

def astar_search(model, start, goal):
    """Return path as list of positions from start to goal inclusive, or None."""
    if start == goal:
        return [start]
    if _is_blocked(model, goal):
        return None

    frontier = []
    heapq.heappush(frontier, (0 + heuristic(start, goal), 0, start))
    came_from = {start: None}
    cost_so_far = {start: 0}

    while frontier:
        _, current_cost, current = heapq.heappop(frontier)
        if current == goal:
            # reconstruct
            path = []
            node = current
            while node is not None:
                path.append(node)
                node = came_from[node]
            return list(reversed(path))
        for nxt in _neighbors(model, current):
            # movement cost is the cost of entering nxt
            move_cost = _get_terrain_cost(model, nxt)
            new_cost = cost_so_far[current] + move_cost
            if nxt not in cost_so_far or new_cost < cost_so_far[nxt]:
                cost_so_far[nxt] = new_cost
                priority = new_cost + heuristic(nxt, goal)
                heapq.heappush(frontier, (priority, new_cost, nxt))
                came_from[nxt] = current
    return None
