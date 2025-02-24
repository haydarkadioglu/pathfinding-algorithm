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
        
        # Create the window
        self.screen = pygame.display.set_mode((self.WINDOW_SIZE, self.WINDOW_SIZE))
        pygame.display.set_caption("Pathfinding Grid")

    def draw_grid(self):
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
                
            # Fill the background
            self.screen.fill(self.WHITE)
            
            # Draw the grid
            self.draw_grid()
            
            # Update the display
            pygame.display.flip()

        pygame.quit()