# bouncingboxscene.py
# Sam Gallagher
# 12 April 2018
#
# A scene which has a box bouncing in the frame
from scene import *
from widget import *
from box import *
import math
import random

class BouncingBoxScene(Scene):
    def __init__(self, winsz):
        Scene.__init__(self,winsz)
        
        #Animation state machine
        self.state = "init"

        #Make animation objects
        self.box1 = Box(50,50,300,150, r=0,g=255,b=0,alpha=250)
        self.box2 = Box(400,100,500,200, r=255,g=0,b=0,alpha=0)
        
        #Scene-specific variablesclass Scene(object):class Scene(object):
        self.vx1 = 50 # Box 1 velocities
        self.vy1 = 100
        self.vx2 = 200
        self.vy2 = 0
    
        self.loadwidget = LoadingBar(self.sz)

    def draw(self):
        self.box1.draw()
        self.box2.draw()
        self.loadwidget.draw()

    def update(self,dt):
        # Handle/define scene states
        if self.state == "init":
            self.state = "movebox"

        elif self.state == "movebox":
            self.box1.move(self.vx1*dt,self.vy1*dt)
            self.box2.move(self.vx2*dt, self.vy2*dt)

            deltax = abs(self.box1.getPosX() - self.box2.getPosX())
            deltay = abs(self.box1.getPosY() - self.box2.getPosY())
            origindist = math.sqrt( pow(deltax,2) + pow(deltay,2) )
            self.loadwidget.update(dt, 100*math.exp(-origindist/200))

            if self.box1.outOfBounds(self.sz[0],self.sz[1]) != "none" or self.box2.outOfBounds(self.sz[0],self.sz[1]) != "none":
                self.state = "bounce"

        elif self.state == "bounce":
            if self.box1.outOfBounds(self.sz[0],self.sz[1]) == "x":
                random.seed()
                randr = random.randint(0,255)
                randg = random.randint(0,255)
                randb = random.randint(0,255)
                self.box1.setColor(randr,randg,randb,255)
                self.vx1 = -self.vx1
            elif self.box1.outOfBounds(self.sz[0],self.sz[1]) == "y":
                random.seed()
                randr = random.randint(0,255)
                randg = random.randint(0,255)
                randb = random.randint(0,255)
                self.box1.setColor(randr,randg,randb,255)
                self.vy1 = -self.vy1
            if self.box2.outOfBounds(self.sz[0],self.sz[1]) == "x":
                self.vx2 = -self.vx2
            elif self.box2.outOfBounds(self.sz[0],self.sz[1]) == "y":
                self.vy2 = -self.vy2
            self.state = "movebox"

        elif self.state == "stop":
            self.state = "stop"


