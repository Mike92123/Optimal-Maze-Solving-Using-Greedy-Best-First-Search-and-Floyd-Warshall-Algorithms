def is_valid(x, y, matrix):
    rows, cols = len(matrix), len(matrix[0])
    return 0 <= y < rows and 0 <= x < cols and matrix[y][x] == 1

def floyd_warshall(matrix):
    INF = float('inf')

    num_vertices = 0
    index_to_coords = {}
    coords_to_index = {}
    rows, cols = len(matrix), len(matrix[0])
    
    for y in range(rows):
        for x in range(cols):
            if matrix[y][x] == 1:
                index_to_coords[num_vertices] = (y, x)
                coords_to_index[(y, x)] = num_vertices
                num_vertices += 1

    dist_matrix = [[INF for _ in range(num_vertices)] for _ in range(num_vertices)]
    pred_matrix = [[None for _ in range(num_vertices)] for _ in range(num_vertices)]
    for i in range(num_vertices):
        dist_matrix[i][i] = 0

    for node, (y, x) in index_to_coords.items():
        neighbors = [(y - 1, x), (y + 1, x), (y, x - 1), (y, x + 1)]
        for ny, nx in neighbors:
            if (ny, nx) in coords_to_index:
                neighbor_node = coords_to_index[(ny, nx)]
                dist_matrix[node][neighbor_node] = 1
                pred_matrix[node][neighbor_node] = node

    for k in range(num_vertices):
        for i in range(num_vertices):
            for j in range(num_vertices):
                if dist_matrix[i][k] + dist_matrix[k][j] < dist_matrix[i][j]:
                    dist_matrix[i][j] = dist_matrix[i][k] + dist_matrix[k][j]
                    pred_matrix[i][j] = pred_matrix[k][j]

    return dist_matrix, pred_matrix, index_to_coords, coords_to_index


def reconstruct_path(start, end, pred_matrix, coords_to_index):
    start_index = coords_to_index[start]
    end_index = coords_to_index[end]
    
    path = []
    current = end_index
    while current is not None:
        path.append(current)
        current = pred_matrix[start_index][current]
    
    path = path[::-1]  # Reverse the path to start-to-goal order
    
    return path
