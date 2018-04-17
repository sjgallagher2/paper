# boxpop.py
# Sam Gallagher
# 16 April 2018
#
# A scene with a box popping up after a delay
from paper.core import Scene
from paper.primitives import Box
import math

class BoxPopScene(Scene):
    def __init__(self,winsz,delay,posx,posy):
        Scene.__init__(self,winsz)
        self.state_ = "init"

        self.boxlen = 100
        self.boxheight = 100
        self.box1 = Box(posx,posy,self.boxlen,self.boxheight,r=0,g=0,b=0)
        self.delaytime = delay #Delay in seconds
        self.tcount = 0.0

    def draw(self):
        self.box1.draw()

    def update(self,dt):
        if self.state_ == "init":
            self.state_ = "wait"
        elif self.state_ == "wait":
            if self.tcount > self.delaytime:
                self.tcount = 0.0
                self.state_ = "setvisible"
            else:
                self.tcount = self.tcount + dt
        elif self.state_ == "setvisible":
            #Pop box into existance
            self.box1.setColor(120,0,120,255)
            self.state_ = "pop"
        elif self.state_ == "pop":
            self.tcount = self.tcount + dt
            scalefactor = 1 + 0.3*math.exp(-3*self.tcount)*math.sin(15*self.tcount)
            if self.tcount < 1.5:
                self.box1.setSize(self.boxlen*scalefactor,self.boxheight*scalefactor,centered=True)
            else:
                self.box1.setSize(self.boxlen,self.boxheight,centered=True)
                self.state_ = "default"
        elif self.state_ == "default":
            pass

