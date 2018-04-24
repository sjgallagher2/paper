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
                #self.state_ = "setvisible"
                self.state_ = "fadein"
            else:
                self.tcount = self.tcount + dt

        elif self.state_ == "setvisible":
            #Pop box into existance
            self.box1.setColor(120,0,120,255)
            self.state_ = "pop"

        elif self.state_ == "pop":
            self.tcount = self.tcount + dt
            if self.box1.popUpState(self.tcount,1.5,self.boxlen,self.boxheight,intensity=0.3,damping=8) > 0:
                pass
            else:
                self.tcount = 0.0
                self.state_ = "wait2"

        elif self.state_ == "fadein":
            self.tcount = self.tcount + dt
            if self.box1.fadeState(self.tcount,dt,1.5,[0,0,0,255],[120,0,120,255]) > 0:
                pass
            else:
                self.tcount = 0.0
                self.state_ = "wait2"


        elif self.state_ == "wait2":
            self.tcount = self.tcount + dt
            if self.tcount > 2:
                self.tcount = 0.0
                #self.state_ = "unpop"
                self.state_ = "fadeout"
            else:
                self.tcount = self.tcount + dt

        elif self.state_ == "unpop":
            self.tcount = self.tcount + dt
            scalefactor = 1 + 0.3*math.exp(5*self.tcount)*math.sin(15*self.tcount)
            if self.box1.getHeight() > 1:
                self.box1.setSize(self.boxlen*scalefactor,self.boxheight*scalefactor,centered=True)
            else:
                self.box1.setColor(r=0,g=0,b=0,alpha=255)
                self.state_ = "wait3"

        elif self.state_ == "fadeout":
            self.tcount = self.tcount + dt
            if self.box1.fadeState(self.tcount,dt,1.5,[120,0,120,255],[0,0,0,255],) > 0:
                pass
            else:
                self.state_ = "wait3"
        
        elif self.state_ == "wait3":
            self.tcount = self.tcount + dt
            if self.tcount > 4:
                self.tcount = 0.0
                #self.state_ = "setvisible"
                self.state_ = "fadein"
            else:
                self.tcount = self.tcount + dt

        elif self.state_ == "default":
            pass

