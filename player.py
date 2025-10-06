#!/usr/bin/env python3

from ursina import Entity, time

class Player(Entity):

    def __init__(self, grid_size=2, grid_x_min=-25, grid_x_max=25, grid_y_min=-10, grid_y_max=10, **kwargs):
        super().__init__()
        self.model = 'quad'
        self.texture = 'assets/player_up.png' # Default player texture
        self.scale_y = 2
        self.scale_x = 2
        self.position = (0, 0, 0)
        self.collider = 'box'
        self.grid_size = grid_size
        self.grid_x_min = grid_x_min
        self.grid_x_max = grid_x_max
        self.grid_y_min = grid_y_min
        self.grid_y_max = grid_y_max
        self.target_pos = self.position.xy
        self.moving = False
        self.move_speed = 10  # units per second

        self.held_direction = None  # Track held direction

        for key, value in kwargs.items():
            setattr(self, key, value)

    def input(self, key):
        # Set held direction on key down, clear on key up
        if key == 'w':
            self.held_direction = 'up'
        elif key == 's':
            self.held_direction = 'down'
        elif key == 'a':
            self.held_direction = 'left'
        elif key == 'd':
            self.held_direction = 'right'
        elif key == 'w up' and self.held_direction == 'up':
            self.held_direction = None
        elif key == 's up' and self.held_direction == 'down':
            self.held_direction = None
        elif key == 'a up' and self.held_direction == 'left':
            self.held_direction = None
        elif key == 'd up' and self.held_direction == 'right':
            self.held_direction = None

    def update(self):
        # Smoothly move to the target position
        if self.moving:
            current = self.position.xy
            target = self.target_pos
            dx = target[0] - current[0]
            dy = target[1] - current[1]
            dist = (dx**2 + dy**2) ** 0.5
            step = self.move_speed * time.dt
            if dist <= step:
                self.position = (target[0], target[1], self.position.z)
                self.moving = False
            else:
                nx = current[0] + dx/dist * step
                ny = current[1] + dy/dist * step
                self.position = (nx, ny, self.position.z)

        # If not moving, check if a direction is held and move again
        if not self.moving and self.held_direction:
            x, y = self.target_pos
            if self.held_direction == 'up' and y + self.grid_size <= self.grid_y_max:
                self.texture = 'assets/player_up.png'
                self.target_pos = (x, y + self.grid_size)
                self.moving = True
            elif self.held_direction == 'down' and y - self.grid_size >= self.grid_y_min:
                self.texture = 'assets/player_down.png'
                self.target_pos = (x, y - self.grid_size)
                self.moving = True
            elif self.held_direction == 'left' and x - self.grid_size >= self.grid_x_min:
                self.texture = 'assets/player_left.png'
                self.target_pos = (x - self.grid_size, y)
                self.moving = True
            elif self.held_direction == 'right' and x + self.grid_size <= self.grid_x_max:
                self.texture = 'assets/player_right.png'
                self.target_pos = (x + self.grid_size, y)
                self.moving = True
