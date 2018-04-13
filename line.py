# line.py
# Sam Gallagher
# 12 April 2018
#
# Line object for animations
import math
import pyglet as pg

class Line(object):
    def __init__(self, x1,y1, x2,y2, width=1, r=255,g=255,b=255,alpha=255):
        self.verts_ = (x1,y1, x2,y2)
        self.width_ = width
        self.rgba_ = (r, g, b, alpha)
        self.vert_list_ = pg.graphics.vertex_list(2,
            ('v2f',self.verts_),
            ('c4B', self.rgba_ + self.rgba_)
        )
    def draw(self):
        pg.gl.glLineWidth(self.width_)
        self.vert_list_.draw(pg.gl.GL_LINES)
    
    def getPosA(self):
        return self.verts_[0:2]
    def getPosB(self):
        return self.verts_[2:4]
    def getLength(self):
        deltax = self.verts_[2] - self.verts_[0]
        deltay = self.verts_[3] - self.verts_[1]
        norm = math.sqrt(math.pow(deltax,2) + math.pow(deltay,2))
        return norm
    def getAngle(self, radians=True):
        deltax = self.verts_[2] - self.verts_[0]
        deltay = self.verts_[3] - self.verts_[1]
        arg = math.atan(deltay/deltax)
        if deltax < 0:
            arg = arg + math.pi
        if radians == False:
            arg = arg*180/math.pi
        return arg
    
    def setPosA(self,x,y):
        self.verts_ = (x,y) + self.verts_[2:4]
        self.vert_list_.vertices = self.verts_
    def setPosB(self,x,y):
        self.verts_ = self.verts_[0:2] + (x,y)
        self.vert_list_.vertices = self.verts_
    def setPos(self,x1,y1,x2,y2):
        self.verts_ = (x1,y1, x2,y2)
        self.vert_list_.vertices = self.verts_
    def setColor(self,r,g,b,alpha):
        rgba = (r,g,b,alpha)
        self.vert_list_.colors = rgba + rgba
    def setWidth(self,w):
        self.width_ = w
