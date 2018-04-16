# widget.py
# Sam Gallagher
# 12 April 2018
#
# A type of scene which serves a repeatable function. Widgets are scenes, the only
# difference is the context you use them in. Any scene can be used as a widget, but
# you should subclass widgets instead for better organization.

from animation.scene.scene import *
from animation.box import *

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
    def __init__(self,winsz,posx,posy,height, barcolor = [0,255,0]):
        Scene.__init__(self,winsz)
        self.posx_ = posx
        self.posy_ = posy
        self.height_ = height
        self.width_ = 0.16*self.height_
        self.barr_ = barcolor[0]
        self.barg_ = barcolor[1]
        self.barb_ = barcolor[2]

        #Initialize objects
        self.outline_ = Box(self.posx_,self.posy_, self.width_,self.height_)
        self.emptybar_ = Box(self.posx_+self.width_/4,self.posy_+self.width_/4, 
                            self.width_/2,self.height_-self.width_/2, 
                            r=0,g=0,b=0)
        self.progress_ = Box(self.posx_+self.width_/4,self.posy_+self.width_/4,
                            self.width_/2,self.height_-self.width_/2, 
                            r=self.barr_,g=self.barg_,b=self.barb_)
    
    def draw(self):
        #Draw objects
        self.outline_.draw()
        self.emptybar_.draw()
        self.progress_.draw()
    
    def update(self, dt, prog):
        if self.state_ == "init":
            #Initial state
            self.progress_.setSize(self.progress_.getLength(), 1)
            self.state_ = "load"
        elif self.state_ == "load":
            self.progress_.setSize(self.progress_.getLength(), self.emptybar_.getHeight()*(prog/100.0))
            if self.progress_.getHeight() >= self.emptybar_.getHeight():
                self.state_ = "init"
    
    def getPosX(self):
        return self.posx_
    def getPosY(self):
        return self.posy_
    def setPosX(self,posx):
        self.posx_ = posx
        self.outline_.move(self.posx_ - self.outline_.getPosX(),0)
        self.emptybar_.move(self.posx_ + self.width_/4 - self.emptybar_.getPosX(),0)
        self.progress_.move(self.posx_ + self.width_/4 - self.progress_.getPosX(),0)
    def setPosY(self,posy):
        self.posy_ = posy
        self.outline_.move(0,self.posy_ - self.outline_.getPosY())
        self.emptybar_.move(0,self.posy_ + self.width_/4 - self.emptybar_.getPosY())
        self.progress_.move(0,self.posy_ + self.width_/4 - self.progress_.getPosY())


