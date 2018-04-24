# htmcolanimation.py
# Sam Gallagher
# 17 April 2018
#
# Test animation for an HTM column

import pyglet
from paper.core import AnimationWindow
from paper.scenes.htmscenes import ColumnScene,SpatialPoolerScene

class HTMColAnim(AnimationWindow):
    def __init__(self,saveanimation=False,filename="",*args,**kwargs):
        AnimationWindow.__init__(self,saveanimation,filename,*args, **kwargs)
        self.scene1 = ColumnScene(self.get_size())
    
    def on_key_press(self,symbol,mods):
        if symbol == pyglet.window.key.ESCAPE:
            #Quit
            self.saveAnimation()
            pyglet.app.exit()
        else:
            self.scene1.update(0,keypress=True)

    def on_draw(self):
        self.clear()
        self.scene1.draw()
    
    def update(self,dt):
        self.scene1.update(dt)
        if self.dosave:
            self.saveframe()


if __name__ == '__main__':
    master = HTMColAnim(True,"columnintro",1200,600)
    pyglet.clock.schedule_interval(master.update,1/120.0)
    pyglet.app.run()