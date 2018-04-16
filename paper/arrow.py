# arrow.py
# Sam Gallagher
# 12 April 2018
#
# Arrow object for animations

from paper.line import *
import pyglet as pg
import math

# The arrow object is a line with a triangle at its tip. The length of the line
# is shortened by the width of the line to give the tip a sharp point. The end
# position is at the tip. Headsize adjusts the length of the arrowhead, but does
# not change the angle of the head. Headang is the angle of the arrow in DEGREES,
# which is converted to radians.

class Arrow(Line):
    def __init__(self, x1,y1, x2,y2, headsize=30,headang=30,width=1, r=255,g=255,b=255,alpha=255):
        Line.__init__(self,x1,y1,x2,y2,width,r,g,b,alpha)
        self.headsize_ = headsize
        self.headang_ = headang*math.pi/180
        self.angle_ = self.getAngle()
        
        self.arrowhead_ = pg.graphics.vertex_list(3,
            ('v2f',self.getHeadVerts()),
            ('c4B',self.rgba_ + self.rgba_ + self.rgba_)
        )
    
    def draw(self):
        pg.gl.glLineWidth(self.width_)
        self.vert_list_.draw(pg.gl.GL_LINES)
        self.arrowhead_.draw(pg.gl.GL_POLYGON)
    
    def setPosA(self,x,y):
        self.verts_ = (x,y) + self.verts_[2:4]
        self.vert_list_.vertices = self.verts_
        self.arrowhead_.vertices = self.getHeadVerts()
    def setPosB(self,x,y):
        self.angle_ = self.getAngle()
        x = x - self.width_*math.cos(self.angle_)
        y = y - self.width_*math.sin(self.angle_)
        self.verts_ = self.verts_[0:2] + (x,y)
        self.vert_list_.vertices = self.verts_
        self.arrowhead_.vertices = self.getHeadVerts()
    def setPos(self,x1,y1,x2,y2):
        self.angle_ = self.getAngle()
        x2 = x2 - self.width_*math.cos(self.angle_)
        y2 = y2 - self.width_*math.sin(self.angle_)
        self.verts_ = (x1,y1, x2,y2)
        self.vert_list_.vertices = self.verts_
        self.arrowhead_.vertices = self.getHeadVerts()
    def setColor(self,r,g,b,alpha):
        rgba = (r,g,b,alpha)
        self.vert_list_.colors = rgba + rgba

    def getHeadVerts(self):
        self.angle_ = self.getAngle()
        tipCX = self.verts_[2] + self.width_*math.cos(self.angle_)
        tipCY = self.verts_[3] + self.width_*math.sin(self.angle_)

        tipAngleA = self.angle_ - self.headang_
        tipAngleB = self.angle_ + self.headang_
        tipLength = self.headsize_

        tipAX = tipLength*math.cos(tipAngleA)
        tipAY = tipLength*math.sin(tipAngleA)
        tipBX = tipLength*math.cos(tipAngleB)
        tipBY = tipLength*math.sin(tipAngleB)

        tipAX = tipCX - tipAX
        tipAY = tipCY - tipAY
        tipBX = tipCX - tipBX
        tipBY = tipCY - tipBY
        tipVerts = (tipCX,tipCY,tipAX,tipAY,tipBX,tipBY)
        return tipVerts