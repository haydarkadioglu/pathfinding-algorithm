import pygame
from grid import GridGUI
from collections import OrderedDict
from typing import List, Tuple, Dict

class StopsMode(GridGUI):
    def __init__(self, window_size, grid_size):
        super().__init__(window_size, grid_size)
        
        # Override menu options to include both connection and pathfinding
        self.MENU_OPTIONS = ["Select Start", "Select End", "Add Stop", 
                           "Connect Stops", "A* Path", "Dijkstra", "Clear All"]
        
        # Add new attributes for stops mode
        self.stops = OrderedDict()  # Dictionary to store stops with order
        self.connections = {}  # Dictionary to store connections between stops
        self.available_numbers = []  # List to track available numbers
        self.selected_stop = None  # For connecting stops
        self.is_connecting = False  # Flag for connection mode

        # Add new color for stops
        self.ORANGE = (255, 165, 0)  # Color for stops

    def add_stop(self, cell_pos):
        """Add a stop with the lowest available number"""
        if self.available_numbers:
            number = min(self.available_numbers)
            self.available_numbers.remove(number)
        else:
            number = len(self.stops) + 1
        self.stops[cell_pos] = number

    def remove_stop(self, cell_pos):
        """Remove a stop and make its number available"""
        if cell_pos in self.stops:
            number = self.stops[cell_pos]
            self.available_numbers.append(number)
            self.stops.pop(cell_pos)

    def handle_grid_click(self, pos):
        if pos[1] < self.MENU_HEIGHT:
            return

        cell_pos = self.get_cell_position(pos)
        if not (0 <= cell_pos[0] < self.GRID_SIZE and 0 <= cell_pos[1] < self.GRID_SIZE):
            return

        if self.selected_option == 0:  # Start position
            if cell_pos not in self.stops:
                if self.start_pos in self.connections:
                    self.connections.pop(self.start_pos)
                self.start_pos = cell_pos
                self.path = []
                self.visited_cells = set()
        elif self.selected_option == 1:  # End position
            if cell_pos not in self.stops:
                if self.end_pos in self.connections:
                    self.connections.pop(self.end_pos)
                self.end_pos = cell_pos
                self.path = []
                self.visited_cells = set()
        elif self.selected_option == 2:  # Add/Remove stop
            if cell_pos != self.start_pos and cell_pos != self.end_pos:
                if cell_pos in self.stops:
                    # Remove stop and its connections
                    self.remove_stop(cell_pos)
                    if cell_pos in self.connections:
                        # Remove connections to this stop from other stops
                        connected_stops = self.connections[cell_pos].copy()  # Create copy to avoid modification during iteration
                        for connected_stop in connected_stops:
                            if connected_stop in self.connections:
                                self.connections[connected_stop].remove(cell_pos)
                                if not self.connections[connected_stop]:
                                    self.connections.pop(connected_stop)
                        self.connections.pop(cell_pos)
                else:
                    # Add new stop
                    self.add_stop(cell_pos)

        elif self.selected_option == 3:  # Connect/Disconnect stops
            if cell_pos in self.stops or cell_pos == self.start_pos or cell_pos == self.end_pos:
                if not self.is_connecting:
                    self.selected_stop = cell_pos
                    self.is_connecting = True
                else:
                    if cell_pos != self.selected_stop:
                        # Check if connection already exists
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

    def draw_grid(self):
        # Fill background with white
        pygame.draw.rect(self.screen, self.WHITE, 
                        (0, self.MENU_HEIGHT, self.WINDOW_SIZE, self.WINDOW_SIZE))

        # Draw menu first
        self.draw_menu()  # Make sure menu is drawn

        # Draw grid lines
        for x in range(0, self.WINDOW_SIZE, self.CELL_SIZE):
            pygame.draw.line(self.screen, self.GRAY, 
                           (x, self.MENU_HEIGHT), 
                           (x, self.WINDOW_SIZE + self.MENU_HEIGHT))
        for y in range(self.MENU_HEIGHT, self.WINDOW_SIZE + self.MENU_HEIGHT, self.CELL_SIZE):
            pygame.draw.line(self.screen, self.GRAY, 
                           (0, y), 
                           (self.WINDOW_SIZE, y))

        # Draw connections between stops with costs
        for stop1, connected_stops in self.connections.items():
            for stop2 in connected_stops:
                # Calculate line start and end points
                x1 = stop1[0] * self.CELL_SIZE + self.CELL_SIZE // 2
                y1 = stop1[1] * self.CELL_SIZE + self.MENU_HEIGHT + self.CELL_SIZE // 2
                x2 = stop2[0] * self.CELL_SIZE + self.CELL_SIZE // 2
                y2 = stop2[1] * self.CELL_SIZE + self.MENU_HEIGHT + self.CELL_SIZE // 2
                
                # Draw connection line
                pygame.draw.line(self.screen, self.BLUE, (x1, y1), (x2, y2), 2)
                
                # Calculate and draw cost
                cost = abs(stop2[0] - stop1[0]) + abs(stop2[1] - stop1[1])  # Manhattan distance
                mid_x = (x1 + x2) // 2
                mid_y = (y1 + y2) // 2
                
                # Draw cost background (small white rectangle)
                text = self.font.render(str(cost), True, self.BLACK)
                text_rect = text.get_rect(center=(mid_x, mid_y))
                padding = 2
                bg_rect = pygame.Rect(text_rect.x - padding,
                                    text_rect.y - padding,
                                    text_rect.width + 2 * padding,
                                    text_rect.height + 2 * padding)
                pygame.draw.rect(self.screen, self.WHITE, bg_rect)
                
                # Draw cost number
                self.screen.blit(text, text_rect)

        # Draw visited cells and path
        for cell in self.visited_cells:
            self.draw_cell(cell, self.LIGHT_BLUE)
        for cell in self.path:
            self.draw_cell(cell, self.YELLOW)

        # Draw stops with numbers
        for stop_pos, stop_num in self.stops.items():
            self.draw_cell(stop_pos, self.ORANGE)
            text = self.font.render(str(stop_num), True, self.BLACK)
            x = stop_pos[0] * self.CELL_SIZE + self.CELL_SIZE // 2
            y = stop_pos[1] * self.CELL_SIZE + self.MENU_HEIGHT + self.CELL_SIZE // 2
            text_rect = text.get_rect(center=(x, y))
            self.screen.blit(text, text_rect)

        # Draw start and end positions
        if self.start_pos:
            self.draw_cell(self.start_pos, self.GREEN)
        if self.end_pos:
            self.draw_cell(self.end_pos, self.RED)

        # Highlight selected stop
        if self.selected_stop:
            rect = (self.selected_stop[0] * self.CELL_SIZE, 
                   self.selected_stop[1] * self.CELL_SIZE + self.MENU_HEIGHT,
                   self.CELL_SIZE, self.CELL_SIZE)
            pygame.draw.rect(self.screen, self.YELLOW, rect, 3)

    def clear_all(self):
        """Override clear all to reset available numbers"""
        super().clear_all()
        self.stops.clear()
        self.connections.clear()
        self.available_numbers = []
        self.selected_stop = None
        self.is_connecting = False

    def draw_menu(self):
        # Calculate button width based on number of options
        button_width = self.WINDOW_SIZE // len(self.MENU_OPTIONS)
        
        # Draw menu background
        pygame.draw.rect(self.screen, self.WHITE, (0, 0, self.WINDOW_SIZE, self.MENU_HEIGHT))
        
        for i, option in enumerate(self.MENU_OPTIONS):
            # Calculate button position
            x = i * button_width
            rect = pygame.Rect(x, 0, button_width, self.MENU_HEIGHT)
            
            # Draw button background (blue if selected, gray if not)
            color = self.BLUE if i == self.selected_option else self.GRAY
            pygame.draw.rect(self.screen, color, rect)
            
            # Draw button text
            text = self.font.render(option, True, self.WHITE)
            text_rect = text.get_rect(center=(x + button_width//2, self.MENU_HEIGHT//2))
            self.screen.blit(text, text_rect)

    def run(self):
        running = True
        while running:
            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    running = False
                
                elif event.type == pygame.MOUSEBUTTONDOWN:
                    mouse_pos = pygame.mouse.get_pos()
                    
                    # Handle menu clicks
                    menu_option = self.get_menu_option(mouse_pos)
                    if menu_option != -1:
                        if menu_option == 4:  # A* Path
                            self.run_pathfinding(use_astar=True)
                        elif menu_option == 5:  # Dijkstra
                            self.run_pathfinding(use_astar=False)
                        elif menu_option == 6:  # Clear All
                            self.clear_all()
                        else:
                            self.selected_option = menu_option
                            self.selected_stop = None
                            self.is_connecting = False
                        continue

                    # Handle grid clicks
                    self.handle_grid_click(mouse_pos)

            # Update display
            self.draw_grid()
            pygame.display.flip()

        pygame.quit()