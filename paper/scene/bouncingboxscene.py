# bouncingboxscene.py
# Sam Gallagher
# 12 April 2018
#
# A scene which has a box bouncing in the frame
from paper.scene.scene import *
from paper.widget.widget import *
from paper.box import *
from paper.arrow import *
from paper.circle import *
import math
import random

class BouncingBoxScene(Scene):
    def __init__(self, winsz):
        Scene.__init__(self,winsz)
        
        #Animation state machine
        self.state_ = "init"

        #Make animation objects
        self.box1 = Box(50,50,300,150, r=0,g=255,b=0,alpha=250)
        self.box2 = Box(400,100,500,200, r=255,g=0,b=0,alpha=0)
        self.line1 = Arrow(50,50,400,100,width=10,headsize=20)
        self.circle1 = Circle(600,200,50)
        self.loadwidget = LoadingBar(self.sz_,100,150,50)
        
        #Scene-specific variablesclass Scene(object):class Scene(object):
        self.vx1 = 50 # Box 1 velocities
        self.vy1 = 100
        self.vx2 = 200
        self.vy2 = 0
    

    def draw(self):
        self.box1.draw()
        self.circle1.draw()
        self.line1.draw()
        self.box2.draw()
        self.loadwidget.draw()

    def update(self,dt):
        # Handle/define scene states
        if self.state_ == "init":
            self.state_ = "movebox"

        elif self.state_ == "movebox":
            self.box1.move(self.vx1*dt,self.vy1*dt)
            self.box2.move(self.vx2*dt, self.vy2*dt)
            self.line1.setPosA(self.box1.getPosX(),self.box1.getPosY())
            self.line1.setPosB(self.box2.getPosX(),self.box2.getPosY())
            self.loadwidget.setPosX(self.box2.getPosX() + 20)
            self.loadwidget.setPosY(self.box2.getPosY() + 20)

            deltax = abs(self.box1.getPosX() - self.box2.getPosX())
            deltay = abs(self.box1.getPosY() - self.box2.getPosY())
            origindist = math.sqrt( pow(deltax,2) + pow(deltay,2) )
            self.loadwidget.update(dt, 100*math.exp(-origindist/200))

            if self.box1.outOfBounds(self.sz_[0],self.sz_[1]) != "none" or self.box2.outOfBounds(self.sz_[0],self.sz_[1]) != "none":
                self.state_ = "bounce"

        elif self.state_ == "bounce":
            if self.box1.outOfBounds(self.sz_[0],self.sz_[1]) == "x":
                random.seed()
                randr = random.randint(0,255)
                randg = random.randint(0,255)
                randb = random.randint(0,255)
                self.box1.setColor(randr,randg,randb,255)
                self.vx1 = -self.vx1
            elif self.box1.outOfBounds(self.sz_[0],self.sz_[1]) == "y":
                random.seed()
                randr = random.randint(0,255)
                randg = random.randint(0,255)
                randb = random.randint(0,255)
                self.box1.setColor(randr,randg,randb,255)
                self.vy1 = -self.vy1
            if self.box2.outOfBounds(self.sz_[0],self.sz_[1]) == "x":
                self.vx2 = -self.vx2
            elif self.box2.outOfBounds(self.sz_[0],self.sz_[1]) == "y":
                self.vy2 = -self.vy2
            self.state_ = "movebox"

        elif self.state_ == "stop":
            self.state_ = "stop"


