# animation.py
# Sam Gallagher
# 11 April 2018

# Window class for animation with Pyglet

import pyglet as pg 

class AnimationWindow(pg.window.Window):
    def __init__(self, *args, **kwargs):
        super(AnimationWindow, self).__init__(*args, **kwargs)
        self.scene1 = None

    def on_draw(self):
        self.clear()
        #self.scene1.draw()

    def update(self,dt):
        pass
        #self.scene1.update(dt)
