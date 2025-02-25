import pygame

class Grid:
    def __init__(self, window_size, grid_size):
        # Initialize Pygame
        pygame.init()
        pygame.font.init()  # Specifically initialize the font module
        
        self.WINDOW_SIZE = window_size
        self.GRID_SIZE = grid_size
        self.CELL_SIZE = window_size // grid_size
        
        # Colors
        self.WHITE = (255, 255, 255)
        self.BLACK = (0, 0, 0)
        self.GRAY = (128, 128, 128)
        self.GREEN = (0, 255, 0)  # Start point
        self.RED = (255, 0, 0)    # End point
        self.BLUE = (50, 50, 200)  # Menu selection
        
        # Create the window with extra height for menu
        self.MENU_HEIGHT = 40
        self.screen = pygame.display.set_mode((self.WINDOW_SIZE, self.WINDOW_SIZE + self.MENU_HEIGHT))
        pygame.display.set_caption("Pathfinding Grid")

        # Initialize points and walls
        self.start_pos = None
        self.end_pos = None
        self.walls = set()
        
        # Menu options
        self.MENU_OPTIONS = ["Select Start", "Select End", "Select Wall"]
        self.selected_option = 0
        self.font = pygame.font.Font(None, 24)

    def draw_menu(self):
        button_width = self.WINDOW_SIZE // len(self.MENU_OPTIONS)
        for i, option in enumerate(self.MENU_OPTIONS):
            color = self.BLUE if i == self.selected_option else self.GRAY
            pygame.draw.rect(self.screen, color, 
                           (i * button_width, 0, button_width, self.MENU_HEIGHT))
            
            text = self.font.render(option, True, self.WHITE)
            text_rect = text.get_rect(center=(i * button_width + button_width//2, self.MENU_HEIGHT//2))
            self.screen.blit(text, text_rect)

    def get_menu_option(self, pos):
        if pos[1] < self.MENU_HEIGHT:
            return pos[0] // (self.WINDOW_SIZE // len(self.MENU_OPTIONS))
        return -1

    def get_cell_position(self, mouse_pos):
        x, y = mouse_pos
        grid_x = x // self.CELL_SIZE
        grid_y = (y - self.MENU_HEIGHT) // self.CELL_SIZE
        return (grid_x, grid_y)

    def draw_cell(self, pos, color):
        x, y = pos
        rect = (x * self.CELL_SIZE, 
               y * self.CELL_SIZE + self.MENU_HEIGHT, 
               self.CELL_SIZE - 1, 
               self.CELL_SIZE - 1)
        pygame.draw.rect(self.screen, color, rect)

    def draw_grid(self):
        # Fill background
        pygame.draw.rect(self.screen, self.WHITE, 
                        (0, self.MENU_HEIGHT, self.WINDOW_SIZE, self.WINDOW_SIZE))
        
        # Draw cells
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

    def run(self):
        running = True
        while running:
            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    running = False
                
                if event.type == pygame.MOUSEBUTTONDOWN:
                    mouse_pos = pygame.mouse.get_pos()
                    
                    # Check if clicking menu
                    menu_option = self.get_menu_option(mouse_pos)
                    if menu_option != -1:
                        self.selected_option = menu_option
                        continue

                    # Handle grid clicks
                    if mouse_pos[1] > self.MENU_HEIGHT:
                        cell_pos = self.get_cell_position(mouse_pos)
                        if 0 <= cell_pos[0] < self.GRID_SIZE and 0 <= cell_pos[1] < self.GRID_SIZE:
                            if self.selected_option == 0:  # Start
                                if cell_pos != self.end_pos and cell_pos not in self.walls:
                                    self.start_pos = cell_pos
                            elif self.selected_option == 1:  # End
                                if cell_pos != self.start_pos and cell_pos not in self.walls:
                                    self.end_pos = cell_pos
                            elif self.selected_option == 2:  # Wall
                                if cell_pos != self.start_pos and cell_pos != self.end_pos:
                                    if cell_pos in self.walls:
                                        self.walls.remove(cell_pos)
                                    else:
                                        self.walls.add(cell_pos)
            
            # Draw everything
            self.draw_menu()
            self.draw_grid()
            pygame.display.flip()

        pygame.quit()