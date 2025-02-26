from typing import List, Set, Dict, Tuple
import heapq

class Dijkstra:
    def __init__(self, grid_size: int):
        self.grid_size = grid_size

    def get_neighbors(self, pos: Tuple[int, int]) -> List[Tuple[int, int]]:
        """Returns valid neighboring positions"""
        x, y = pos
        neighbors = []
        
        # Check all 8 surrounding positions (including diagonals)
        for dx, dy in [(0, 1), (1, 0), (0, -1), (-1, 0), (1, 1), (-1, 1), (1, -1), (-1, -1)]:
            new_x, new_y = x + dx, y + dy
            if 0 <= new_x < self.grid_size and 0 <= new_y < self.grid_size:
                neighbors.append((new_x, new_y))
        return neighbors

    def find_path(self, start: Tuple[int, int], end: Tuple[int, int], walls: Set[Tuple[int, int]]) -> List[Tuple[int, int]]:
        """Find shortest path using Dijkstra's algorithm"""
        frontier = []
        heapq.heappush(frontier, (0, start))
        
        came_from: Dict[Tuple[int, int], Tuple[int, int]] = {}
        cost_so_far: Dict[Tuple[int, int], float] = {}
        
        came_from[start] = None
        cost_so_far[start] = 0

        while frontier:
            current = heapq.heappop(frontier)[1]

            if current == end:
                break

            for next_pos in self.get_neighbors(current):
                if next_pos in walls:
                    continue

                # Diagonal movement costs more (√2 ≈ 1.414)
                is_diagonal = abs(next_pos[0] - current[0]) == 1 and abs(next_pos[1] - current[1]) == 1
                new_cost = cost_so_far[current] + (1.414 if is_diagonal else 1.0)

                if next_pos not in cost_so_far or new_cost < cost_so_far[next_pos]:
                    cost_so_far[next_pos] = new_cost
                    priority = new_cost  # Priority is just the cost (no heuristic)
                    heapq.heappush(frontier, (priority, next_pos))
                    came_from[next_pos] = current

        # Reconstruct path
        path = []
        current = end
        while current is not None:
            path.append(current)
            current = came_from.get(current)
        
        path.reverse()
        return path if path[0] == start else []