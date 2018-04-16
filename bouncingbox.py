# bouncingbox.py
# Sam Gallagher
# 16 April 2018
#
# Bouncing box animation

import pyglet as pg
from paper.animationwindow import *
from paper.scene.bouncingboxscene import *

class BouncingBoxAnimation(AnimationWindow):
    def __init__(self,*args,**kwargs):
        super(BouncingBoxAnimation, self).__init__(*args, **kwargs)
        self.scene1 = BouncingBoxScene(self.get_size())

    def on_draw(self):
        self.clear()
        self.scene1.draw()

    def update(self,dt):
        self.scene1.update(dt)

if __name__ == '__main__':
    master = BouncingBoxAnimation(1200,600)
    pg.clock.schedule_interval(master.update,1/120.0)
    pg.app.run()
