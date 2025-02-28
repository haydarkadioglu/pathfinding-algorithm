import pygame
from grid import GridGUI

class StopsGUI(GridGUI):
    def __init__(self, window_size, grid_size):
        super().__init__(window_size, grid_size)
        self.ORANGE = (255, 165, 0)  # Color for stops
        self.MENU_OPTIONS = ["Select Start", "Select End", "Add Stop", 
                           "Connect Stops", "A* Path", "Dijkstra", "Clear All"]
        self.selected_option = 0
        self.logic = None
        self.is_dragging = False
        self.drag_start = None

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
                            self.logic.find_path_through_stops(use_astar=True)
                        elif menu_option == 5:  # Dijkstra
                            self.logic.find_path_through_stops(use_astar=False)
                        elif menu_option == 6:  # Clear All
                            self.logic.clear_all()
                        else:
                            self.selected_option = menu_option
                        continue

                    # Start dragging in connect mode
                    if self.selected_option == 3:
                        self.is_dragging = True
                        self.drag_start = mouse_pos
                        self.logic.start_connection(mouse_pos)

                elif event.type == pygame.MOUSEBUTTONUP:
                    if self.is_dragging and self.selected_option == 3:
                        self.is_dragging = False
                        self.logic.end_connection(pygame.mouse.get_pos())
                        self.drag_start = None

                elif event.type == pygame.MOUSEMOTION:
                    if self.is_dragging and self.selected_option == 3:
                        self.logic.update_connection(pygame.mouse.get_pos())

            # Update display
            self.draw_grid()
            
            # Draw connection preview line while dragging
            if self.is_dragging and self.drag_start and self.selected_option == 3:
                mouse_pos = pygame.mouse.get_pos()
                pygame.draw.line(self.screen, self.BLUE, self.drag_start, mouse_pos, 2)
            
            pygame.display.flip()

        pygame.quit()

    def get_menu_option(self, pos):
        """Returns which menu option was clicked (-1 if none)"""
        if pos[1] < self.MENU_HEIGHT:
            return pos[0] // (self.WINDOW_SIZE // len(self.MENU_OPTIONS))
        return -1

    def draw_grid(self):
        # Fill background with white
        pygame.draw.rect(self.screen, self.WHITE, 
                        (0, self.MENU_HEIGHT, self.WINDOW_SIZE, self.WINDOW_SIZE))

        self.draw_menu()
        self._draw_grid_lines()
        self._draw_connections()
        self._draw_visited_and_path()
        self._draw_stops()
        self._draw_start_end()
        self._draw_selected_stop()

    def _draw_grid_lines(self):
        # Draw grid lines
        for x in range(0, self.WINDOW_SIZE, self.CELL_SIZE):
            pygame.draw.line(self.screen, self.GRAY, 
                           (x, self.MENU_HEIGHT), 
                           (x, self.WINDOW_SIZE + self.MENU_HEIGHT))
        for y in range(self.MENU_HEIGHT, self.WINDOW_SIZE + self.MENU_HEIGHT, self.CELL_SIZE):
            pygame.draw.line(self.screen, self.GRAY, 
                           (0, y), 
                           (self.WINDOW_SIZE, y))

    def _draw_connections(self):
        for stop1, connected_stops in self.logic.connections.items():
            for stop2 in connected_stops:
                self._draw_connection(stop1, stop2)

    def _draw_connection(self, stop1, stop2):
        x1 = stop1[0] * self.CELL_SIZE + self.CELL_SIZE // 2
        y1 = stop1[1] * self.CELL_SIZE + self.MENU_HEIGHT + self.CELL_SIZE // 2
        x2 = stop2[0] * self.CELL_SIZE + self.CELL_SIZE // 2
        y2 = stop2[1] * self.CELL_SIZE + self.MENU_HEIGHT + self.CELL_SIZE // 2
        
        pygame.draw.line(self.screen, self.BLUE, (x1, y1), (x2, y2), 2)
        
        # Draw connection cost
        cost = abs(stop2[0] - stop1[0]) + abs(stop2[1] - stop1[1])
        self._draw_cost(cost, (x1 + x2) // 2, (y1 + y2) // 2)

    def _draw_cost(self, cost, x, y):
        text = self.font.render(str(cost), True, self.BLACK)
        text_rect = text.get_rect(center=(x, y))
        padding = 2
        bg_rect = pygame.Rect(text_rect.x - padding,
                            text_rect.y - padding,
                            text_rect.width + 2 * padding,
                            text_rect.height + 2 * padding)
        pygame.draw.rect(self.screen, self.WHITE, bg_rect)
        self.screen.blit(text, text_rect)

    def _draw_visited_and_path(self):
        for cell in self.logic.visited_cells:
            self.draw_cell(cell, self.LIGHT_BLUE)
        for cell in self.logic.path:
            self.draw_cell(cell, self.YELLOW)

    def _draw_stops(self):
        for stop_pos, stop_num in self.logic.stops.items():
            self.draw_cell(stop_pos, self.ORANGE)
            text = self.font.render(str(stop_num), True, self.BLACK)
            x = stop_pos[0] * self.CELL_SIZE + self.CELL_SIZE // 2
            y = stop_pos[1] * self.CELL_SIZE + self.MENU_HEIGHT + self.CELL_SIZE // 2
            text_rect = text.get_rect(center=(x, y))
            self.screen.blit(text, text_rect)

    def _draw_start_end(self):
        if self.logic.start_pos:
            self.draw_cell(self.logic.start_pos, self.GREEN)
        if self.logic.end_pos:
            self.draw_cell(self.logic.end_pos, self.RED)

    def _draw_selected_stop(self):
        if self.logic.selected_stop:
            rect = (self.logic.selected_stop[0] * self.CELL_SIZE, 
                   self.logic.selected_stop[1] * self.CELL_SIZE + self.MENU_HEIGHT,
                   self.CELL_SIZE, self.CELL_SIZE)
            pygame.draw.rect(self.screen, self.YELLOW, rect, 3)