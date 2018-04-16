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

class Scene(object):
    def __init__(self, winsz):
        #Window size
        self.sz_ = winsz
        self.state_ = "init"

    def draw(self):
        # Draw all objects
        pass
    def update(self,dt):
        # Handle/define scene states
        if self.state_ == "init":
            self.state_ = "init"