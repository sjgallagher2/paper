# widget.py
# Sam Gallagher
# 12 April 2018
#
# A type of scene which serves a repeatable function. Widgets are scenes, the only
# difference is the context you use them in. Any scene can be used as a widget, but
# you should subclass widgets instead for better organization.

from scene import *
from box import *

class Widget(Scene):
    def __init__(self,winsz):
        Scene.__init__(self,winsz)

        #Initialize objects
    def draw(self):
        #Draw objects
        pass
    def update(self,dt):
        #Update based on input params
        pass


class LoadingBar(Widget):
    def __init__(self,winsz):
        Scene.__init__(self,winsz)

        #Initialize objects
        self.outline = Box(100,100,40,300)
        self.emptybar = Box(110,110,20,280,r=0,g=0,b=0)
        self.progress = Box(110,110,20,280,r=0,g=255,b=0)
    
    def draw(self):
        #Draw objects
        self.outline.draw()
        self.emptybar.draw()
        self.progress.draw()
    
    def update(self, dt, prog):
        if self.state == "init":
            #Initial state
            self.progress.setSize(self.progress.getLength(), 1)
            self.state = "load"
        elif self.state == "load":
            self.progress.setSize(self.progress.getLength(), self.emptybar.getHeight()*(prog/100.0))
            if self.progress.getHeight() >= self.emptybar.getHeight():
                self.state = "init"