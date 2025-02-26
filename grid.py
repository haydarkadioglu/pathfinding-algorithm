import pygame
import time
from pathfinder import PathFinder

class GridGUI:
    def __init__(self, window_size, grid_size):
        # Initialize Pygame
        pygame.init()
        pygame.font.init()
        
        # Grid parameters
        self.WINDOW_SIZE = window_size
        self.GRID_SIZE = grid_size
        self.CELL_SIZE = window_size // grid_size
        self.MENU_HEIGHT = 40
        
        # States
        self.visited_cells = set()
        self.is_drawing = False
        self.current_cell = None
        self.path = []
        self.start_pos = None
        self.end_pos = None
        self.walls = set()
        self.last_wall_pos = None  # Add this to track last wall position

        # Colors
        self.WHITE = (255, 255, 255)
        self.BLACK = (0, 0, 0)
        self.GRAY = (128, 128, 128)
        self.GREEN = (0, 255, 0)
        self.RED = (255, 0, 0)
        self.BLUE = (50, 50, 200)
        self.LIGHT_BLUE = (100, 100, 255)
        self.YELLOW = (255, 255, 0)
        self.DARK_BLUE = (0, 0, 150)

        # Setup display
        self.screen = pygame.display.set_mode((self.WINDOW_SIZE, self.WINDOW_SIZE + self.MENU_HEIGHT))
        pygame.display.set_caption("Pathfinding Visualization")

        # Menu setup
        self.MENU_OPTIONS = ["Select Start", "Select End", "Select Wall", "A* Path", "Dijkstra", "Clear All"]
        self.selected_option = 0
        self.font = pygame.font.Font(None, 24)

        # Initialize pathfinder
        self.pathfinder = PathFinder(grid_size)

    def draw_cell(self, pos, color):
        """Draw a single cell at the given position"""
        if 0 <= pos[0] < self.GRID_SIZE and 0 <= pos[1] < self.GRID_SIZE:
            rect = (pos[0] * self.CELL_SIZE, 
                   pos[1] * self.CELL_SIZE + self.MENU_HEIGHT,
                   self.CELL_SIZE - 1, 
                   self.CELL_SIZE - 1)
            pygame.draw.rect(self.screen, color, rect)

    def handle_grid_click(self, pos):
        """Handle clicks on the grid"""
        if pos[1] < self.MENU_HEIGHT:
            return

        cell_pos = self.get_cell_position(pos)
        if not (0 <= cell_pos[0] < self.GRID_SIZE and 0 <= cell_pos[1] < self.GRID_SIZE):
            return

        if self.selected_option == 0:  # Start position
            if cell_pos != self.end_pos and cell_pos not in self.walls:
                self.start_pos = cell_pos
                self.path = []
                self.visited_cells = set()
        elif self.selected_option == 1:  # End position
            if cell_pos != self.start_pos and cell_pos not in self.walls:
                self.end_pos = cell_pos
                self.path = []
                self.visited_cells = set()
        elif self.selected_option == 2:  # Wall
            if cell_pos != self.start_pos and cell_pos != self.end_pos:
                if cell_pos in self.walls:
                    self.walls.remove(cell_pos)
                else:
                    self.walls.add(cell_pos)
                self.path = []
                self.visited_cells = set()

    def clear_all(self):
        """Reset all grid states"""
        self.start_pos = None
        self.end_pos = None
        self.walls.clear()
        self.path = []
        self.visited_cells = set()
        self.current_cell = None
        self.pathfinder = PathFinder(self.GRID_SIZE)

    def interpolate_line(self, start, end):
        """Interpolate all points between start and end positions"""
        points = []
        x1, y1 = start
        x2, y2 = end
        
        dx = abs(x2 - x1)
        dy = abs(y2 - y1)
        x, y = x1, y1
        
        step_x = 1 if x1 < x2 else -1
        step_y = 1 if y1 < y2 else -1
        
        if dx > dy:
            err = dx / 2
            while x != x2:
                points.append((x, y))
                err -= dy
                if err < 0:
                    y += step_y
                    err += dx
                x += step_x
        else:
            err = dy / 2
            while y != y2:
                points.append((x, y))
                err -= dx
                if err < 0:
                    x += step_x
                    err += dy
                y += step_y
                
        points.append((x2, y2))
        return points

    def handle_wall_drawing(self, pos):
        """Handle wall drawing with interpolation"""
        current_cell = self.get_cell_position(pos)
        
        if not (0 <= current_cell[0] < self.GRID_SIZE and 0 <= current_cell[1] < self.GRID_SIZE):
            return
            
        if current_cell == self.start_pos or current_cell == self.end_pos:
            return

        if self.last_wall_pos and self.last_wall_pos != current_cell:
            # Interpolate between last position and current position
            wall_points = self.interpolate_line(self.last_wall_pos, current_cell)
            for point in wall_points:
                if point != self.start_pos and point != self.end_pos:
                    self.walls.add(point)
        else:
            self.walls.add(current_cell)
            
        self.last_wall_pos = current_cell

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
                        if menu_option == 3:  # A* Path
                            self.run_pathfinding(use_astar=True)
                        elif menu_option == 4:  # Dijkstra
                            self.run_pathfinding(use_astar=False)
                        elif menu_option == 5:  # Clear All
                            self.clear_all()
                        else:
                            self.selected_option = menu_option
                            self.last_wall_pos = None  # Reset wall tracking
                        continue

                    # Handle grid clicks
                    self.handle_grid_click(mouse_pos)
                    if self.selected_option == 2:  # Wall option
                        self.last_wall_pos = self.get_cell_position(mouse_pos)
                
                elif event.type == pygame.MOUSEBUTTONUP:
                    self.last_wall_pos = None  # Reset wall tracking
                    
                elif event.type == pygame.MOUSEMOTION:
                    if pygame.mouse.get_pressed()[0] and self.selected_option == 2:
                        self.handle_wall_drawing(pygame.mouse.get_pos())

            # Update display
            self.draw_menu()
            self.draw_grid()
            pygame.display.flip()

        pygame.quit()

    def draw_menu(self):
        # Calculate button width based on number of options
        button_width = self.WINDOW_SIZE // len(self.MENU_OPTIONS)
        
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

    def get_menu_option(self, pos):
        """Returns which menu option was clicked (-1 if none)"""
        if pos[1] < self.MENU_HEIGHT:
            return pos[0] // (self.WINDOW_SIZE // len(self.MENU_OPTIONS))
        return -1
    
    def get_cell_position(self, mouse_pos):
        x, y = mouse_pos
        grid_x = x // self.CELL_SIZE
        grid_y = (y - self.MENU_HEIGHT) // self.CELL_SIZE
        return (grid_x, grid_y)
    
    def draw_grid(self):
        # Fill background
        pygame.draw.rect(self.screen, self.WHITE, 
                        (0, self.MENU_HEIGHT, self.WINDOW_SIZE, self.WINDOW_SIZE))
        
        # Draw visited cells
        for cell in self.visited_cells:
            self.draw_cell(cell, self.LIGHT_BLUE)

        # Draw current cell being processed
        if self.current_cell:
            self.draw_cell(self.current_cell, self.DARK_BLUE)

        # Draw final path
        for cell in self.path:
            self.draw_cell(cell, self.YELLOW)
        
        # Draw start, end and walls
        if self.start_pos:
            self.draw_cell(self.start_pos, self.GREEN)
        if self.end_pos:
            self.draw_cell(self.end_pos, self.RED)
        for wall in self.walls:
            self.draw_cell(wall, self.BLACK)

        # Draw grid lines
        for x in range(0, self.WINDOW_SIZE, self.CELL_SIZE):
            pygame.draw.line(self.screen, self.GRAY, 
                           (x, self.MENU_HEIGHT), 
                           (x, self.WINDOW_SIZE + self.MENU_HEIGHT))
        for y in range(self.MENU_HEIGHT, self.WINDOW_SIZE + self.MENU_HEIGHT, self.CELL_SIZE):
            pygame.draw.line(self.screen, self.GRAY, 
                           (0, y), 
                           (self.WINDOW_SIZE, y))

    def run_pathfinding(self, use_astar=True):
        if not self.start_pos or not self.end_pos:
            return

        # Reset previous path and visited cells
        self.path = []
        self.visited_cells = set()
        self.current_cell = None

        # Update pathfinder with current grid state
        self.pathfinder.start_pos = self.start_pos
        self.pathfinder.end_pos = self.end_pos
        self.pathfinder.walls = self.walls.copy()

        # Run pathfinding algorithm with animation
        for step_type, position in self.pathfinder.find_path_animated(use_astar):
            if step_type == "visit":
                self.current_cell = position
                self.visited_cells.add(position)
            elif step_type == "path":
                self.path.append(position)
            
            # Draw current state
            self.draw_grid()
            pygame.display.flip()
            pygame.event.pump()  # Process events to keep window responsive
            time.sleep(0.05)  # Add delay for animation

        # Clear current cell after finishing
        self.current_cell = None