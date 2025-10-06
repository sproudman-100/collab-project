#!/usr/bin/env python3

from ursina import Entity, Grid, color

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