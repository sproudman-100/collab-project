from ursina import Ursina, camera

from player import Player
from background import Background
from ursina import Ursina, Entity, time, color, camera, held_keys, Grid
import random

class Player(Entity):

    def __init__(self, grid_size=2, grid_x_min=-25, grid_x_max=25, grid_y_min=-10, grid_y_max=10, **kwargs):
        super().__init__()
        self.model = 'quad'
        self.texture = 'assets/player_up.png'
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

        for key, value in kwargs.items():
            setattr(self, key, value)

    def input(self, key):
        if self.moving:
            return
        x, y = self.target_pos
        if key == 'w' and y + self.grid_size <= self.grid_y_max:
            self.texture = 'assets/player_up.png'
            self.target_pos = (x, y + self.grid_size)
            self.moving = True
        elif key == 's' and y - self.grid_size >= self.grid_y_min:
            self.texture = 'assets/player_down.png'
            self.target_pos = (x, y - self.grid_size)
            self.moving = True
        elif key == 'a' and x - self.grid_size >= self.grid_x_min:
            self.texture = 'assets/player_left.png'
            self.target_pos = (x - self.grid_size, y)
            self.moving = True
        elif key == 'd' and x + self.grid_size <= self.grid_x_max:
            self.texture = 'assets/player_right.png'
            self.target_pos = (x + self.grid_size, y)
            self.moving = True

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

# Create a tree entity
class Tree(Entity):
    def __init__(self, **kwargs):
        super().__init__()
        self.model = 'cube'
        self.scale_y = 4
        self.scale_x = 4
        self.collider = 'box'
        self.texture = 'assets/tree.png'
        for key, value in kwargs.items():
            setattr(self, key, value)

class Background():
    def __init__(self, enable_grid=True):
        # Tile the grass background image across the entire screen
        tile_size = 10  # Adjust to match the aspect ratio of your grass.jpg
        tiles_x = 10   # Number of tiles horizontally
        tiles_y = 5   # Number of tiles vertically
        for x in range(-tiles_x//2, tiles_x//2+1):
            for y in range(-tiles_y//2, tiles_y//2+1):
                Entity(
                    model='quad',
                    texture='assets/grass.jpg',
                    scale=(tile_size, tile_size, 1),
                    position=(x*tile_size, y*tile_size, 1),
                    collider=None
                )
        if enable_grid:
            # Calculate the grid range to cover the same area as the background tiles
            grid_scale = 2
            grid_x_min = (-tiles_x//2) * tile_size // grid_scale
            grid_x_max = (tiles_x//2) * tile_size // grid_scale
            grid_y_min = (-tiles_y//2) * tile_size // grid_scale
            grid_y_max = (tiles_y//2) * tile_size // grid_scale
            for x in range(grid_x_min, grid_x_max+1):
                for y in range(grid_y_min, grid_y_max+1):
                    Entity(
                        model=Grid(1, 1),
                        scale=(grid_scale, grid_scale),
                        position=(x*grid_scale, y*grid_scale, 0.5),
                        color=color.rgba(255,255,255,30)
                    )


if __name__ == '__main__':
    app = Ursina(title='PyZelda', borderless=False, fullscreen=False, vsync=True, show_ursina_splash=False)
    camera.orthographic = True

    background = Background(enable_grid=True)

    player = Player()
    # Set grid bounds to match the grid in Background
    player = Player(grid_size=2, grid_x_min=-25, grid_x_max=25, grid_y_min=-10, grid_y_max=10)

    # Insert Tree entities at random positions
    tree_count = 10
    for i in range(tree_count):
        Tree(position=(random.uniform(-20, 20), random.uniform(-20, 20), 0), collider='box')
    


    app.run()

