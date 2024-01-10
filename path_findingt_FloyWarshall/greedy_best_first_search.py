import heapq


def is_valid(x, y, matrix):
    rows, cols = len(matrix), len(matrix[0])
    return 0 <= y < rows and 0 <= x < cols and matrix[y][x] == 1


def greedy_best_first_search(matrix, start, goal):
    visited = set()
    priority_queue = []
    heapq.heappush(priority_queue, (0, start))  # Priority queue format: (heuristic, (x, y))

    while priority_queue:
        _, current = heapq.heappop(priority_queue)
        x, y = current

        if current == goal:
            return True  # Path found

        visited.add(current)

        neighbors = [
            (y, x - 1),  # Left
            (y, x + 1),  # Right
            (y - 1, x),  # Up
            (y + 1, x)   # Down
        ]

        for neighbor in neighbors:
            nx, ny = neighbor
            if is_valid(nx, ny, matrix) and neighbor not in visited:
                priority = abs(nx - goal[0]) + abs(ny - goal[1])  # Manhattan distance heuristic
                heapq.heappush(priority_queue, (priority, neighbor))
                visited.add(neighbor)

    return False  # Path not found


def find_path(matrix, start, goal):
    if not is_valid(*start, matrix) or not is_valid(*goal, matrix):
        return None

    if start == goal:
        return [start]

    if not greedy_best_first_search(matrix, start, goal):
        return None

    parent_map = {}

    priority_queue = []
    heapq.heappush(priority_queue, (0, start))  # Priority queue format: (heuristic, (x, y))

    while priority_queue:
        _, current = heapq.heappop(priority_queue)
        x, y = current

        if current == goal:
            break

        neighbors = [
            (y, x - 1),  # Left
            (y, x + 1),  # Right
            (y - 1, x),  # Up
            (y + 1, x)   # Down
        ]

        for neighbor in neighbors:
            nx, ny = neighbor
            if is_valid(nx, ny, matrix) and neighbor not in parent_map:
                priority = abs(ny - goal[1]) + abs(nx - goal[0])   # Manhattan distance heuristic
                heapq.heappush(priority_queue, (priority, neighbor))
                parent_map[neighbor] = current

    path = []
    current = goal
    while current != start:
        path.append(current)
        current = parent_map[current]
    path.append(start)
    path.reverse()
    return path
