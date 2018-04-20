# lineextendscene.py
# Sam Gallagher
# 19 April 2018
#
# A scene with a line that extends outwards
from paper.core import Scene
from paper.primitives import Line,Arrow
import math

class LineExtendScene(Scene):
    def __init__(self,winsz):
        Scene.__init__(self,winsz)
        
        self.lineX = 400
        self.lineY = 300
        self.linePos = [50,50]
        self.delaytime = 3.5
        self.telapsed = 0.0
        #self.line1 = Line(self.linePos[0],self.linePos[1],self.linePos[0]+5,self.linePos[1]+5,width=5,r=0,g=0,b=0)
        self.line1 = Arrow(self.linePos[0],self.linePos[1],self.linePos[0]+5,self.linePos[1]+5,width=5,r=0,g=0,b=0,headsize=15)
    
    def draw(self):
        self.line1.draw()
    
    def update(self,dt):
        if self.state_ == "init":
            self.state_ = "wait"
        elif self.state_ == "wait":
            if self.telapsed > self.delaytime:
                self.telapsed = 0.0
                self.state_ = "setvisible"
            else:
                self.telapsed = self.telapsed + dt
        
        elif self.state_ == "setvisible":
            self.line1.setColor(255,255,255,255)
            self.state_ = "extend"
        
        elif self.state_ == "extend":
            self.telapsed = self.telapsed + dt
            if self.line1.extendState(self.telapsed,dt,0.5,self.lineX,self.lineY) == 1:
                pass
            else:
                self.state_ = "default"
        
        elif self.state_ == "default":
            pass