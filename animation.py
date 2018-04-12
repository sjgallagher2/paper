# animation.py
# Sam Gallagher
# 11 April 2018

# Window class for animation with Pyglet

import pyglet as pg 
from bouncingboxscene import *

class Animation(pg.window.Window):
    def __init__(self, *args, **kwargs):
        super(Animation, self).__init__(*args, **kwargs)
        self.scene1 = BouncingBoxScene(self.get_size())

    def on_draw(self):
        self.clear()
        self.scene1.draw()

    def update(self,dt):
        self.scene1.update(dt)

if __name__ == '__main__':
    master = Animation(1200,600)
    pg.clock.schedule_interval(master.update,1/120.0)
    pg.app.run()