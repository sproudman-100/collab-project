from ursina import Ursina, camera

from player import Player
from background import Background


if __name__ == '__main__':
    app = Ursina(title='PyZelda', borderless=False, fullscreen=False, vsync=True, show_ursina_splash=False)
    camera.orthographic = True

    background = Background(enable_grid=True)

    player = Player()

    app.run()

