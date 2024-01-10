import heapq


def is_valid(x, y, matrix):
    rows, cols = len(matrix), len(matrix[0])
    return 0 <= y < rows and 0 <= x < cols and matrix[y][x] == 1


def greedy_best_first_search(matrix, start, goal):
    visited = set()
    priority_queue = []
    heapq.heappush(priority_queue, (0, start))  # Priority queue format: (heuristic, (x, y))

    while priority_queue:
        #pop the node with the lowest heuristic value
        _, current = heapq.heappop(priority_queue)
        x, y = current
        
        if current == goal:
            return True  # Path found
        #add current node to the visisted set
        visited.add(current)
        
        #define the neighboring position fo the current node
        neighbors = [
            (x - 1, y),
            (x + 1, y),
            (x, y - 1),
            (x, y + 1)
        ]


        for neighbor in neighbors:
            nx, ny = neighbor

            #check neighbour is valid and not visited
            if is_valid(nx, ny, matrix) and neighbor not in visited:
                priority = abs(nx - goal[0]) + abs(ny - goal[1])  # Manhattan distance heuristic
                heapq.heappush(priority_queue, (priority, neighbor))
                visited.add(neighbor)

    return False  # Path not found


def find_path(matrix, start, goal):
    #check if start and end nodes are valid on the marix
    if not is_valid(*start, matrix) or not is_valid(*goal, matrix):
        return None

    #return start node if start and end nodes are the same
    if start == goal:
        return [start]

    #path not exist by GBFS
    if not greedy_best_first_search(matrix, start, goal):
        return None
    
    #Closed List
    parent_map = {}

    #Open List
    priority_queue = []

    #Priority queue with 'Start'position
    heapq.heappush(priority_queue, (0, start))  # Priority queue format: (heuristic, (x, y))

    while priority_queue:
        _, current = heapq.heappop(priority_queue)
        x, y = current

        if current == goal:
            break
        #4 direction neighbours
        neighbors = [
            (x - 1, y), 
            (x + 1, y),
            (x, y - 1),
            (x, y + 1)
        ]

        for neighbor in neighbors:
            nx, ny = neighbor
            if is_valid(nx, ny, matrix) and neighbor not in parent_map:
                priority = abs(nx - goal[0]) + abs(ny - goal[1])  # Manhattan distance heuristic
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
