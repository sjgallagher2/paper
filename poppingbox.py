
# bouncingbox.py
# Sam Gallagher
# 16 April 2018
#
# Bouncing box animation

import pyglet as pg
from paper.core import AnimationWindow
from paper.scenes.boxpop import BoxPopScene

class PoppingBoxAnimation(AnimationWindow):
    def __init__(self,*args,**kwargs):
        super(PoppingBoxAnimation, self).__init__(*args, **kwargs)
        self.scene1 = BoxPopScene(self.get_size(),1.5,200,300)
        self.scene2 = BoxPopScene(self.get_size(),1.8,350,300)
        self.scene3 = BoxPopScene(self.get_size(),2.1,500,300)
        self.scene4 = BoxPopScene(self.get_size(),2.4,650,300)
        self.scene5 = BoxPopScene(self.get_size(),2.7,800,300)

    def on_draw(self):
        self.clear()
        self.scene1.draw()
        self.scene2.draw()
        self.scene3.draw()
        self.scene4.draw()
        self.scene5.draw()

    def update(self,dt):
        self.scene1.update(dt)
        self.scene2.update(dt)
        self.scene3.update(dt)
        self.scene4.update(dt)
        self.scene5.update(dt)

if __name__ == '__main__':
    master = PoppingBoxAnimation(1200,600)
    pg.clock.schedule_interval(master.update,1/120.0)
    pg.app.run()
