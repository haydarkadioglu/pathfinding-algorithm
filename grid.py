import pygame

class Grid:
    def __init__(self, window_size, grid_size):
        self.WINDOW_SIZE = window_size
        self.GRID_SIZE = grid_size
        self.CELL_SIZE = window_size // grid_size
        
        # Colors
        self.WHITE = (255, 255, 255)
        self.BLACK = (0, 0, 0)
        self.GRAY = (128, 128, 128)
        self.GREEN = (0, 255, 0)  # Start point
        self.RED = (255, 0, 0)    # End point
        
        # Create the window
        self.screen = pygame.display.set_mode((self.WINDOW_SIZE, self.WINDOW_SIZE))
        pygame.display.set_caption("Pathfinding Grid")

        # Initialize start and end points
        self.start_pos = None
        self.end_pos = None

    def get_cell_position(self, mouse_pos):
        x, y = mouse_pos
        grid_x = x // self.CELL_SIZE
        grid_y = y // self.CELL_SIZE
        return (grid_x, grid_y)

    def draw_cell(self, pos, color):
        x, y = pos
        rect = (x * self.CELL_SIZE, y * self.CELL_SIZE, self.CELL_SIZE, self.CELL_SIZE)
        pygame.draw.rect(self.screen, color, rect)

    def draw_grid(self):
        # Draw cells first
        if self.start_pos:
            self.draw_cell(self.start_pos, self.GREEN)
        if self.end_pos:
            self.draw_cell(self.end_pos, self.RED)

        # Draw grid lines
        for x in range(0, self.WINDOW_SIZE, self.CELL_SIZE):
            pygame.draw.line(self.screen, self.GRAY, (x, 0), (x, self.WINDOW_SIZE))
        for y in range(0, self.WINDOW_SIZE, self.CELL_SIZE):
            pygame.draw.line(self.screen, self.GRAY, (0, y), (self.WINDOW_SIZE, y))

    def run(self):
        running = True
        while running:
            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    running = False
                
                if event.type == pygame.MOUSEBUTTONDOWN:
                    cell_pos = self.get_cell_position(pygame.mouse.get_pos())
                    
                    # Left click for start point
                    if event.button == 1:
                        if cell_pos != self.end_pos:  # Prevent overlapping
                            self.start_pos = cell_pos
                    
                    # Right click for end point
                    elif event.button == 3:
                        if cell_pos != self.start_pos:  # Prevent overlapping
                            self.end_pos = cell_pos
            
            # Fill the background
            self.screen.fill(self.WHITE)
            
            # Draw the grid
            self.draw_grid()
            
            # Update the display
            pygame.display.flip()

        pygame.quit()