import heapq
from typing import Set, Tuple, List, Dict
from astar import AStar
from dijkstra import Dijkstra

class PathFinder:
    def __init__(self, grid_size: int):
        self.grid_size = grid_size
        self.start_pos = None
        self.end_pos = None
        self.walls = set()
        self.visited_cells = set()
        self.path = []
        self.current_cell = None

    def find_path(self, use_astar=True):
        if not self.start_pos or not self.end_pos:
            return False

        # Clear previous results
        self.visited_cells = set()
        self.path = []

        # Initialize algorithm
        if use_astar:
            from astar import AStar
            algorithm = AStar(self.grid_size)
        else:
            from dijkstra import Dijkstra
            algorithm = Dijkstra(self.grid_size)

        # Find path
        path = algorithm.find_path(self.start_pos, self.end_pos, self.walls)
        if path:
            self.path = path
            return True
        return False

    def find_path_animated(self, use_astar=True):
        """Animated version of pathfinding that yields each step"""
        if not self.start_pos or not self.end_pos:
            return

        # Initialize algorithm
        if use_astar:
            algorithm = AStar(self.grid_size)
        else:
            algorithm = Dijkstra(self.grid_size)

        # Clear previous results
        self.visited_cells = set()
        self.path = []

        # Initialize search
        frontier = []
        heapq.heappush(frontier, (0, self.start_pos))
        came_from = {self.start_pos: None}
        cost_so_far = {self.start_pos: 0}

        while frontier:
            current = heapq.heappop(frontier)[1]
            yield "visit", current  # Yield each visited cell

            if current == self.end_pos:
                break

            for next_pos in self.get_neighbors(current):
                if next_pos in self.walls:
                    continue

                is_diagonal = abs(next_pos[0] - current[0]) == 1 and abs(next_pos[1] - current[1]) == 1
                new_cost = cost_so_far[current] + (1.414 if is_diagonal else 1.0)

                if next_pos not in cost_so_far or new_cost < cost_so_far[next_pos]:
                    cost_so_far[next_pos] = new_cost
                    priority = new_cost
                    if use_astar:
                        priority += algorithm.heuristic(self.end_pos, next_pos)
                    heapq.heappush(frontier, (priority, next_pos))
                    came_from[next_pos] = current

        # Reconstruct and animate path
        current = self.end_pos
        while current is not None:
            yield "path", current  # Yield each path cell
            current = came_from.get(current)

    def get_neighbors(self, pos):
        x, y = pos
        neighbors = []
        for dx, dy in [(0, 1), (1, 0), (0, -1), (-1, 0), (1, 1), (-1, 1), (1, -1), (-1, -1)]:
            new_x, new_y = x + dx, y + dy
            if (0 <= new_x < self.grid_size and 
                0 <= new_y < self.grid_size and 
                (new_x, new_y) not in self.walls):
                neighbors.append((new_x, new_y))
        return neighbors