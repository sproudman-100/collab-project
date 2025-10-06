from ursina import Ursina, Entity, time, color, camera, held_keys, scene, Sprite

class Player(Entity):

    def __init__(self, **kwargs):
        super().__init__()
        self.model='arrow'
        self.color = color.red
        self.scale_y = 1

        for key, value in kwargs.items():
            setattr(self, key, value)

    def update(self):
        if held_keys['a']:
            self.x -= 2 * time.dt
        if held_keys['d']:
            self.x += 2 * time.dt
        if held_keys['w']:
            self.y += 2 * time.dt
        if held_keys['s']:
            self.y -= 2 * time.dt



if __name__ == '__main__':
    app = Ursina(title='PyZelda', borderless=False, fullscreen=False, vsync=True, show_ursina_splash=False)
    camera.orthographic = True


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

    player = Player(model='cube', color=color.azure, scale_y=1, position=(0,0,0), collider='box')

    app.run()

