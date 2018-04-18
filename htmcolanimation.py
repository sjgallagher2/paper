# htmcolanimation.py
# Sam Gallagher
# 17 April 2018
#
# Test animation for an HTM column

import pyglet
from paper.core import AnimationWindow
from paper.scenes.htmscenes import ColumnTestScene

class HTMColAnim(AnimationWindow):
    def __init__(self,*args,**kwargs):
        AnimationWindow.__init__(self,*args, **kwargs)
        self.scene1 = ColumnTestScene(self.get_size())
    
    def on_draw(self):
        self.clear()
        self.scene1.draw()
    
    def update(self,dt):
        self.scene1.update(dt)

if __name__ == '__main__':
    master = HTMColAnim(1200,600)
    pyglet.clock.schedule_interval(master.update,1/120.0)
    pyglet.app.run()