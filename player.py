
import pygame

class Player:
    def __init__(self, grid_x, grid_y, grid_width, grid_height):
        self.grid_x = grid_x
        self.grid_y = grid_y
        self.grid_width = grid_width
        self.grid_height = grid_height
        self.x = grid_y // 2
        self.y = grid_x // 2

        # Load player sprites
        self.sprites = {
            'up': pygame.image.load('assets/player_up.png').convert_alpha(),
            'down': pygame.image.load('assets/player_down.png').convert_alpha(),
            'left': pygame.image.load('assets/player_left.png').convert_alpha(),
            'right': pygame.image.load('assets/player_right.png').convert_alpha(),
        }
        self.direction = 'down'

        # For smooth movement
        self.animating = False
        self.anim_start_time = 0
        self.anim_duration = 0.1  # seconds
        self.start_px = 0
        self.start_py = 0
        self.target_px = 0
        self.target_py = 0

        # For key hold movement
        self.held_direction = None

        # For collision checking
        self.collidable_objects = []

    def set_collidable_objects(self, objects):
        """Set the list of objects to check collision against"""
        self.collidable_objects = objects

    def can_move_to(self, x, y):
        """Check if the player can move to the given grid position"""
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

    def move(self, dx, dy):
        # Set held direction for continuous movement
        if dx == 1:
            self.held_direction = 'right'
        elif dx == -1:
            self.held_direction = 'left'
        elif dy == 1:
            self.held_direction = 'down'
        elif dy == -1:
            self.held_direction = 'up'

        if self.animating:
            return  # Ignore input while animating
        self._move_in_direction(self.held_direction)

    def stop(self, direction):
        # Stop movement if released key matches held direction
        if self.held_direction == direction:
            self.held_direction = None

    def _move_in_direction(self, direction):
        if direction == 'right':
            dx, dy = 1, 0
            self.direction = 'right'
        elif direction == 'left':
            dx, dy = -1, 0
            self.direction = 'left'
        elif direction == 'down':
            dx, dy = 0, 1
            self.direction = 'down'
        elif direction == 'up':
            dx, dy = 0, -1
            self.direction = 'up'
        else:
            return
        new_x = max(0, min(self.grid_y - 1, self.x + dx))
        new_y = max(0, min(self.grid_x - 1, self.y + dy))

        # Check collision using internal collision checking
        if not self.can_move_to(new_x, new_y):
            return

        if (new_x, new_y) != (self.x, self.y):
            self.animating = True
            self.anim_start_time = pygame.time.get_ticks() / 1000.0
            self.start_px = self.x * self.grid_width
            self.start_py = self.y * self.grid_height
            self.target_px = new_x * self.grid_width
            self.target_py = new_y * self.grid_height
            self.x = new_x
            self.y = new_y

    def update(self):
        # Call this every frame to update animation and handle held key movement
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
            # If a direction is held, move again
            if self.held_direction:
                self._move_in_direction(self.held_direction)

    def draw(self, surface):
        sprite = pygame.transform.scale(self.sprites[self.direction], (self.grid_width, self.grid_height))
        surface.blit(sprite, (self.current_px, self.current_py))