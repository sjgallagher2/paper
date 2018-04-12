# box.py
# Sam Gallagher
# 12 April 2018
#
# A 2D pyglet rectangle/box with position, dimensions, and color
import pyglet as pg


class Box(object):
    def __init__(self,xpos,ypos,length,height,r=255,g=255,b=255,alpha=255):
        self.xpos_ = xpos
        self.ypos_ = ypos
        self.length_ = length
        self.height_ = height

        verts = (self.xpos_,self.ypos_, self.xpos_+self.length_,self.ypos_, self.xpos_+self.length_,self.ypos_+self.height_, self.xpos_,self.ypos_+self.height_)
        self.rgba_ = (r, g, b, alpha)

        self.vert_list_ = pg.graphics.vertex_list(4, 
            ('v2f', verts),
            ('c4B', self.rgba_ + self.rgba_ + self.rgba_ + self.rgba_)  #Color for each vertice
        )

    def draw(self):
        self.vert_list_.draw(pg.gl.GL_POLYGON)

    def getPosX(self):
        return self.xpos_
    def getPosY(self):
        return self.ypos_
    def getLength(self):
        return self.length_
    def getHeight(self):
        return self.height_

    def setPos(self,xpos,ypos):
        self.xpos_ = xpos
        self.ypos_ = ypos
        verts = self.getVerts()
        self.vert_list_.vertices  = verts
    def setSize(self,length,height):
        self.length_ = length
        self.height_ = height
        verts = self.getVerts()
        self.vert_list_.vertices = verts
    def move(self,dx,dy):
        self.xpos_ = self.xpos_ + dx
        self.ypos_ = self.ypos_ + dy
        verts = self.getVerts()
        self.vert_list_.vertices = verts
    def scale(self,lScale,hScale):
        self.length_ = self.length_*lScale
        self.height_ = self.height_*hScale
        verts = self.getVerts()
        self.vert_list_.vertices = verts
    
    def setColor(self,r,g,b,alpha):
        rgba = [r, g, b, alpha]
        self.vert_list_.colors = rgba + rgba + rgba + rgba
    
    def outOfBounds(self, xbound, ybound):
        if self.xpos_ + self.length_ > xbound or self.xpos_ < 0:
            return "x"
        if self.ypos_ + self.height_ > ybound or self.ypos_ < 0:
            return "y"
        else:
            return "none"
    def getVerts(self):
        return [self.xpos_,self.ypos_, self.xpos_+self.length_,self.ypos_, self.xpos_+self.length_,self.ypos_+self.height_, self.xpos_,self.ypos_+self.height_]
