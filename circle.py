# circle.py
# Sam Gallagher
# 12 April 2018
#
# Circle object for animations

# Circles have a fixed radius, and ideally an infinite number of vertices. However,
# we can't actually draw an infinite number of vertices, so we have to approximate. 
# Approximating requires a number of vertices N separated by some constant angle, and
# this can be computationally expensive if we're not careful. A rotation matrix will
# used to calculate the position of the vertices, thus eliminating many expensive sine/cosine
# functions.

import pyglet as pg
import math

class Circle(object):
    def __init__(self, posx,posy,rad,N=30,r=255,g=255,b=255,alpha=255):
        self.posx_ = posx
        self.posy_ = posy
        self.rad_ = rad
        self.nVerts_ = N
        self.rgba_ = [r, g, b, alpha]

        self.theta_ = 2*math.pi/self.nVerts_
        self.cosTheta_ = math.cos(self.theta_)
        self.sinTheta_ = math.sin(self.theta_)

        self.verts_ = self.getVerts_()

        self.vert_list_ = pg.graphics.vertex_list(self.nVerts_,
            ('v2f',self.verts_),
            ('c4B',self.getColors_())
        )

    def draw(self):
        self.vert_list_.draw(pg.gl.GL_POLYGON)
    
    def getPosX(self):
        return self.posx_
    def getPosY(self):
        return self.posy_
    def getRadius(self):
        return self.rad_
    def getNVerts(self):
        return self.nVerts_
    
    def move(self,posx,posy):
        deltax = posx - self.posx_
        deltay = posy - self.posy_
        self.posx_ = posx
        self.posy_ = posy
        
        for i in range(0,self.nVerts_*2,2):
            self.verts_[i] = self.verts_[i] + deltax
            self.verts_[i+1] = self.verts_[i+1] + deltay
        self.vert_list_.vertices = self.verts_
    def setRadius(self,rad):
        self.rad_ = rad
        #Recalculate the circle
        self.vert_list_.vertices = self.getVerts_()
    def scale(self,pct):
        newrad = self.rad_*pct
        self.setRadius(newrad)
    def setNVerts(self,N):
        self.nVerts_ = N
        #Recalculate theta, sin theta, and cos theta
        self.theta_ = 2*math.pi/self.nVerts_
        self.cosTheta_ = math.cos(self.theta_)
        self.sinTheta_ = math.sin(self.theta_)
        #Recalculate vertices and color, make a new vertex list
        self.vert_list_ = pg.graphics.vertex_list(self.nVerts_,
            ('v2f',self.getVerts_()),
            ('c4B',self.getColors_())
        )

    def getVerts_(self):
        #Start with a circle around the origin
        verts = [self.rad_, 0]
        for v in range(2,self.nVerts_*2,2):
            verts.append(verts[v-2] * self.cosTheta_ - verts[v-1] * self.sinTheta_) #append x
            verts.append(verts[v-2] * self.sinTheta_ + verts[v-1] * self.cosTheta_) #append y
        
        #Move vertices to center position
        for j in range(0,self.nVerts_*2,2):
            verts[j] = verts[j] + self.posx_
            verts[j+1] = verts[j+1] + self.posy_
        return verts
    def getColors_(self):
        rgba = self.rgba_
        for i in range(1,self.nVerts_):
            rgba = rgba + self.rgba_
        return rgba
    