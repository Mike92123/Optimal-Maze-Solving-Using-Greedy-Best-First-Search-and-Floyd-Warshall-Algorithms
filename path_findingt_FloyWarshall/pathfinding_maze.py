import sys
import pygame
from pathfinding.core.grid import Grid
from greedy_best_first_search import find_path
from floyd_warshall import reconstruct_path
from floyd_warshall import floyd_warshall

class Pathfinder:
    def __init__(self, mtrix):
        self.matrix = mtrix
        self.grid = Grid(matrix=mtrix)
        self.path = []

    def empty_path(self):
        self.path = []

    def draw_active_cell(self, image, position):
        col = position[0] // 30
        row = position[1] // 30
        current_cell_value = self.matrix[row][col]
        if current_cell_value == 1:
            rect = pygame.Rect((col * 30, row * 30), (30, 30))
            screen.blit(image, rect)

    @staticmethod
    def get_coordinate():
        mouse_pos = pygame.mouse.get_pos()
        x, y = mouse_pos[0] // 30, mouse_pos[1] // 30
        return x, y

    # pathfinder
    def create_path(self, x1, y1, x2, y2, algorithm=None):
        start = (y1, x1)
        end = (y2, x2)

        print("start", start)
        print("end", end)

        if algorithm == "GBFS":
            self.path = find_path(self.matrix, start, end)
        elif algorithm == "FW":
            dist_matrix, pred_matrix, index_to_coords, coords_to_index = floyd_warshall(self.matrix)
            path  = reconstruct_path(start, end, pred_matrix, coords_to_index)
            self.path = [index_to_coords[node_index] for node_index in path]

        print("total cells travelled:", len(self.path))
        print(self.path)
        self.grid.cleanup()

    def draw_path(self):
        if self.path:
            points = []
            for point in self.path:
                # plus 16 to draw the line till the centre of rectangle
                x = (point[0] * 30) + 15
                y = (point[1] * 30) + 15
                points.append((y, x))

            pygame.draw.lines(screen, '#FF0000', False, points, 5)

    def update(self):
        self.draw_path()


def get_matrix():
    return [
        [0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0],
        [0, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 0],
        [0, 1, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 1, 1, 0],
        [0, 1, 0, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 0, 0, 1, 0],
        [0, 1, 0, 1, 1, 1, 1, 0, 1, 1, 0, 0, 0, 0, 0, 1, 0, 1, 1, 0],
        [0, 1, 0, 1, 1, 0, 0, 0, 1, 1, 0, 1, 1, 1, 0, 1, 0, 1, 0, 0],
        [0, 1, 0, 1, 1, 0, 1, 1, 1, 1, 0, 1, 1, 1, 0, 1, 0, 1, 1, 0],
        [0, 1, 0, 0, 0, 0, 1, 0, 0, 0, 0, 0, 0, 1, 0, 1, 0, 1, 1, 0],
        [0, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 0, 1, 0, 1, 0, 0, 1, 0],
        [0, 1, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 1, 0, 1, 0, 1, 1, 0],
        [0, 1, 0, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 0, 1, 0, 1, 1, 0],
        [0, 1, 0, 0, 0, 0, 0, 1, 1, 0, 1, 0, 0, 0, 0, 1, 0, 0, 1, 0],
        [0, 1, 1, 1, 1, 1, 0, 1, 1, 0, 1, 1, 1, 0, 1, 1, 1, 0, 1, 0],
        [0, 1, 0, 0, 0, 1, 0, 1, 0, 0, 0, 0, 0, 0, 1, 1, 1, 0, 1, 0],
        [0, 1, 0, 1, 1, 1, 0, 1, 0, 1, 1, 1, 1, 1, 1, 0, 0, 0, 1, 0],
        [0, 1, 0, 1, 1, 1, 0, 1, 0, 1, 1, 1, 1, 1, 1, 0, 1, 1, 1, 0],
        [0, 1, 0, 0, 0, 0, 0, 1, 0, 0, 0, 0, 0, 0, 0, 0, 1, 0, 0, 0],
        [0, 1, 1, 0, 1, 1, 1, 1, 1, 0, 1, 1, 0, 1, 1, 1, 1, 0, 1, 0],
        [0, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 0],
        [0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0]
    ]


# option: GBFS, FW
ALGORITHM = "FW"

if __name__ == "__main__":
    # pygame setup
    pygame.init()
    screen = pygame.display.set_mode((600, 599))
    clock = pygame.time.Clock()

    # game setup
    bg_surf = pygame.image.load('maze.png').convert()
    pathfinder = Pathfinder(get_matrix())

    # algorithm
    # 1. init board
    # 2. set START point
    # 3. set END point
    # 4. find path with algorithm
    # 5. draw path
    # 6. reset upon next mouse down event for start point

    is_start_point = True
    start_x, start_y = 0, 0

    while True:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                sys.exit()
            if event.type == pygame.MOUSEBUTTONDOWN:
                # start_x, start_y = 0, 0
                if is_start_point:
                    print("setting start point..")
                    start_x, start_y = pathfinder.get_coordinate()
                    # prepare for END point
                    is_start_point = False
                else:
                    print("setting end point..")
                    end_x, end_y = pathfinder.get_coordinate()
                    # prepare for START point again
                    is_start_point = True
                    pathfinder.create_path(start_x, start_y, end_x, end_y, ALGORITHM)

        screen.blit(bg_surf, (0, 0))
        pathfinder.update()

        pygame.display.update()
        clock.tick(60)
