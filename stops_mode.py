import pygame
from grid import GridGUI
from collections import OrderedDict
from typing import List, Tuple, Dict
import time
from stops_gui import StopsGUI

class StopsMode:
    def __init__(self, window_size, grid_size):
        self.gui = StopsGUI(window_size, grid_size)
        self.gui.logic = self
        
        self.grid_size = grid_size
        self.stops = OrderedDict()
        self.connections = {}
        self.available_numbers = []
        self.selected_stop = None
        self.is_connecting = False
        
        self.start_pos = None
        self.end_pos = None
        self.path = []
        self.visited_cells = set()
        self.current_cell = None
        self.temp_connection = None  # Add this line

    def add_stop(self, cell_pos):
        if self.available_numbers:
            number = min(self.available_numbers)
            self.available_numbers.remove(number)
        else:
            number = len(self.stops) + 1
        self.stops[cell_pos] = number

    def remove_stop(self, cell_pos):
        if cell_pos in self.stops:
            number = self.stops[cell_pos]
            self.available_numbers.append(number)
            self.stops.pop(cell_pos)

    def clear_all(self):
        self.stops.clear()
        self.connections.clear()
        self.available_numbers = []
        self.selected_stop = None
        self.is_connecting = False
        self.start_pos = None
        self.end_pos = None
        self.path = []
        self.visited_cells = set()
        self.current_cell = None

    def handle_grid_click(self, pos):
        """Handle grid clicks based on selected option"""
        # Convert screen position to grid position
        cell_pos = (pos[0] // self.gui.CELL_SIZE,
                    (pos[1] - self.gui.MENU_HEIGHT) // self.gui.CELL_SIZE)
        
        if not (0 <= cell_pos[0] < self.grid_size and 0 <= cell_pos[1] < self.grid_size):
            return

        if self.gui.selected_option == 0:  # Start position
            if cell_pos not in self.stops:
                self.start_pos = cell_pos
                self.path = []
                self.visited_cells = set()
        
        elif self.gui.selected_option == 1:  # End position
            if cell_pos not in self.stops:
                self.end_pos = cell_pos
                self.path = []
                self.visited_cells = set()
        
        elif self.gui.selected_option == 2:  # Add/Remove stop
            if cell_pos != self.start_pos and cell_pos != self.end_pos:
                if cell_pos in self.stops:
                    # Remove stop and its connections
                    self.remove_stop(cell_pos)
                    if cell_pos in self.connections:
                        # Remove connections to this stop
                        connected_stops = self.connections[cell_pos].copy()
                        for connected_stop in connected_stops:
                            if connected_stop in self.connections:
                                self.connections[connected_stop].remove(cell_pos)
                                if not self.connections[connected_stop]:
                                    self.connections.pop(connected_stop)
                        self.connections.pop(cell_pos)
                else:
                    # Add new stop
                    self.add_stop(cell_pos)
        
        elif self.gui.selected_option == 3:  # Connect/Disconnect stops
            valid_points = list(self.stops.keys())
            if self.start_pos:
                valid_points.append(self.start_pos)
            if self.end_pos:
                valid_points.append(self.end_pos)
                
            if cell_pos in valid_points:
                if not self.is_connecting:
                    self.selected_stop = cell_pos
                    self.is_connecting = True
                else:
                    if cell_pos != self.selected_stop:
                        # Check if connection exists
                        if (self.selected_stop in self.connections and 
                            cell_pos in self.connections[self.selected_stop]):
                            # Remove existing connection
                            self.connections[self.selected_stop].remove(cell_pos)
                            self.connections[cell_pos].remove(self.selected_stop)
                            # Clean up empty sets
                            if not self.connections[self.selected_stop]:
                                self.connections.pop(self.selected_stop)
                            if not self.connections[cell_pos]:
                                self.connections.pop(cell_pos)
                        else:
                            # Add new connection
                            if self.selected_stop not in self.connections:
                                self.connections[self.selected_stop] = set()
                            if cell_pos not in self.connections:
                                self.connections[cell_pos] = set()
                            self.connections[self.selected_stop].add(cell_pos)
                            self.connections[cell_pos].add(self.selected_stop)
                    self.selected_stop = None
                    self.is_connecting = False

    def finish_connection(self, pos):
        """Finish connecting two stops"""
        cell_pos = (pos[0] // self.gui.CELL_SIZE,
                   (pos[1] - self.gui.MENU_HEIGHT) // self.gui.CELL_SIZE)

        valid_points = list(self.stops.keys())
        if self.start_pos:
            valid_points.append(self.start_pos)
        if self.end_pos:
            valid_points.append(self.end_pos)

        if cell_pos in valid_points and self.selected_stop and cell_pos != self.selected_stop:
            # Check if connection exists
            if (self.selected_stop in self.connections and 
                cell_pos in self.connections[self.selected_stop]):
                # Remove existing connection
                self.connections[self.selected_stop].remove(cell_pos)
                self.connections[cell_pos].remove(self.selected_stop)
                # Clean up empty sets
                if not self.connections[self.selected_stop]:
                    self.connections.pop(self.selected_stop)
                if not self.connections[cell_pos]:
                    self.connections.pop(cell_pos)
            else:
                # Add new connection
                if self.selected_stop not in self.connections:
                    self.connections[self.selected_stop] = set()
                if cell_pos not in self.connections:
                    self.connections[cell_pos] = set()
                self.connections[self.selected_stop].add(cell_pos)
                self.connections[cell_pos].add(self.selected_stop)

        self.selected_stop = None
        self.is_connecting = False

    def start_connection(self, pos):
        """Start creating a connection"""
        cell_pos = (pos[0] // self.gui.CELL_SIZE,
                   (pos[1] - self.gui.MENU_HEIGHT) // self.gui.CELL_SIZE)
        
        valid_points = list(self.stops.keys())
        if self.start_pos:
            valid_points.append(self.start_pos)
        if self.end_pos:
            valid_points.append(self.end_pos)
            
        if cell_pos in valid_points:
            self.selected_stop = cell_pos
            self.is_connecting = True

    def update_connection(self, pos):
        """Update temporary connection preview"""
        if self.is_connecting:
            self.temp_connection = pos

    def end_connection(self, pos):
        """Finish creating a connection"""
        if not self.is_connecting:
            return

        cell_pos = (pos[0] // self.gui.CELL_SIZE,
                   (pos[1] - self.gui.MENU_HEIGHT) // self.gui.CELL_SIZE)

        valid_points = list(self.stops.keys())
        if self.start_pos:
            valid_points.append(self.start_pos)
        if self.end_pos:
            valid_points.append(self.end_pos)

        if cell_pos in valid_points and self.selected_stop and cell_pos != self.selected_stop:
            # Toggle connection
            if (self.selected_stop in self.connections and 
                cell_pos in self.connections[self.selected_stop]):
                # Remove existing connection
                self.connections[self.selected_stop].remove(cell_pos)
                self.connections[cell_pos].remove(self.selected_stop)
                # Clean up empty sets
                if not self.connections[self.selected_stop]:
                    self.connections.pop(self.selected_stop)
                if not self.connections[cell_pos]:
                    self.connections.pop(cell_pos)
            else:
                # Add new connection
                if self.selected_stop not in self.connections:
                    self.connections[self.selected_stop] = set()
                if cell_pos not in self.connections:
                    self.connections[cell_pos] = set()
                self.connections[self.selected_stop].add(cell_pos)
                self.connections[cell_pos].add(self.selected_stop)

        self.selected_stop = None
        self.is_connecting = False
        self.temp_connection = None

    def find_path_through_stops(self, use_astar=True):
        """Find path visiting all connected stops"""
        if not self.start_pos or not self.end_pos:
            return

        # Reset previous path
        self.path = []
        self.visited_cells = set()
        self.current_cell = None

        # Get all stops that are connected (either directly or indirectly)
        connected_stops = set()
        to_visit = {self.start_pos}
        visited = set()
        total_cost = 0

        while to_visit:
            current = to_visit.pop()
            visited.add(current)
            if current in self.connections:
                connected_stops.add(current)
                for next_stop in self.connections[current]:
                    if next_stop not in visited:
                        to_visit.add(next_stop)

        # Create ordered list of points to visit
        points_to_visit = [self.start_pos]
        current_point = self.start_pos

        # Find path through stops
        visited_stops = {self.start_pos}
        path_costs = []  # Store costs between stops

        while len(visited_stops) < len(connected_stops):
            if current_point not in self.connections:
                break

            # Find next stop with lowest cost
            nearest = None
            min_cost = float('inf')
            for next_point in self.connections[current_point]:
                if next_point not in visited_stops:
                    cost = abs(next_point[0] - current_point[0]) + abs(next_point[1] - current_point[1])
                    if cost < min_cost:
                        min_cost = min_cost
                        nearest = next_point

            if nearest:
                points_to_visit.append(nearest)
                path_costs.append(min_cost)
                total_cost += min_cost
                visited_stops.add(nearest)
                current_point = nearest
                
                # Highlight current stop and show cost
                self.current_cell = nearest
                self.visited_cells.add(nearest)
                self.gui.draw_grid()
                pygame.display.flip()
                pygame.event.pump()
                time.sleep(0.5)  # Longer delay to see each stop

        # Add final connection to end point if needed
        if points_to_visit[-1] != self.end_pos:
            points_to_visit.append(self.end_pos)
            final_cost = abs(self.end_pos[0] - points_to_visit[-2][0]) + abs(self.end_pos[1] - points_to_visit[-2][1])
            path_costs.append(final_cost)
            total_cost += final_cost

        # Show final path through stops
        self.path = points_to_visit
        
        # Draw final state with total cost
        font = pygame.font.Font(None, 36)
        text = font.render(f"Total Cost: {total_cost}", True, (0, 0, 0))
        text_rect = text.get_rect(center=(self.gui.WINDOW_SIZE // 2, self.gui.MENU_HEIGHT // 2))
        self.gui.screen.blit(text, text_rect)
        pygame.display.flip()
        time.sleep(2)  # Show total cost for 2 seconds

        self.current_cell = None

    def run(self):
        self.gui.run()