
import pygame
import random

class Enemy:
    def __init__(self, grid_x, grid_y, grid_width, grid_height):
        self.grid_x = grid_x
        self.grid_y = grid_y
        self.grid_width = grid_width
        self.grid_height = grid_height

        # Random spawn position
        self.x = random.randint(0, grid_y - 1)
        self.y = random.randint(0, grid_x - 1)

        # Load enemy sprite
        self.sprite = pygame.image.load('assets/enemy.png').convert_alpha()

        # For smooth movement
        self.animating = False
        self.anim_start_time = 0
        self.anim_duration = 0.15  # slightly slower than player
        self.start_px = 0
        self.start_py = 0
        self.target_px = 0
        self.target_py = 0

        # For random movement
        self.move_timer = 0
        self.move_interval = random.uniform(1.0, 3.0)  # Move every 1-3 seconds

        # For collision checking
        self.collidable_objects = []

    def set_collidable_objects(self, objects):
        """Set the list of objects to check collision against"""
        self.collidable_objects = objects

    def can_move_to(self, x, y):
        """Check if the enemy can move to the given grid position"""
        # Check if position is within bounds
        if x < 0 or x >= self.grid_y or y < 0 or y >= self.grid_x:
            return False

        # Check collision with all collidable objects
        for obj in self.collidable_objects:
            if hasattr(obj, 'get_occupied_cells'):
                occupied_cells = obj.get_occupied_cells()
                if (x, y) in occupied_cells:
                    return False
        return True

    def _move_in_direction(self, dx, dy):
        """Try to move in the given direction"""
        new_x = self.x + dx
        new_y = self.y + dy

        # Check collision
        if not self.can_move_to(new_x, new_y):
            return False

        if (new_x, new_y) != (self.x, self.y):
            self.animating = True
            self.anim_start_time = pygame.time.get_ticks() / 1000.0
            self.start_px = self.x * self.grid_width
            self.start_py = self.y * self.grid_height
            self.target_px = new_x * self.grid_width
            self.target_py = new_y * self.grid_height
            self.x = new_x
            self.y = new_y
            return True
        return False

    def update(self, dt):
        """Update enemy AI and animation"""
        # Update animation
        if self.animating:
            now = pygame.time.get_ticks() / 1000.0
            t = (now - self.anim_start_time) / self.anim_duration
            if t >= 1.0:
                self.animating = False
                self.current_px = self.target_px
                self.current_py = self.target_py
            else:
                self.current_px = self.start_px + (self.target_px - self.start_px) * t
                self.current_py = self.start_py + (self.target_py - self.start_py) * t
        else:
            self.current_px = self.x * self.grid_width
            self.current_py = self.y * self.grid_height

        # Random movement AI
        if not self.animating:
            self.move_timer += dt
            if self.move_timer >= self.move_interval:
                self.move_timer = 0
                self.move_interval = random.uniform(1.0, 3.0)  # Reset interval

                # Try to move in a random direction
                directions = [(0, 1), (0, -1), (1, 0), (-1, 0)]  # down, up, right, left
                random.shuffle(directions)

                for dx, dy in directions:
                    if self._move_in_direction(dx, dy):
                        break

    def get_occupied_cells(self):
        """Return list of (x, y) grid positions occupied by the enemy"""
        return [(self.x, self.y)]

    def draw(self, surface):
        sprite = pygame.transform.scale(self.sprite, (self.grid_width, self.grid_height))
        surface.blit(sprite, (self.current_px, self.current_py))
