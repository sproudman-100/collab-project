from ursina import Ursina, Entity, time, color, camera

class Player(Entity):
    def update(self):
        self.x += 1 * time.dt

if __name__ == '__main__':
    app = Ursina(title='PyZelda')
    
    camera.orthographic = True
    
    ground = Entity(model='cube', color=color.olive.tint(-.4), z=-.1, y=-1, origin_y=.59, scale=(1000,100,10), collider='box', ignore=True)
    player = Player(model='cube', color=color.azure, scale_y=1, position=(0,0,0), collider='box')

    app.run()

