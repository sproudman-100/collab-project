import pygame

class Tree:
    def __init__(self, grid_x, grid_y, grid_width, grid_height):
        self.grid_width = grid_width
        self.grid_height = grid_height
        self.width = 2  # 2 grid spaces wide
        self.height = 3  # 3 grid spaces tall
        self.x = grid_x
        self.y = grid_y

        # Load tree sprite
        self.sprite = pygame.image.load('assets/tree.png').convert_alpha()

    def get_occupied_cells(self):
        """Return list of (x, y) grid positions occupied by the tree"""
        cells = []
        for dx in range(self.width):
            for dy in range(self.height):
                cells.append((self.x + dx, self.y + dy))
        return cells

    def draw(self, surface):
        px = self.x * self.grid_width
        py = self.y * self.grid_height
        sprite = pygame.transform.scale(self.sprite, (self.grid_width * self.width, self.grid_height * self.height))
        surface.blit(sprite, (px, py))