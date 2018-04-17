import math
import pyglet as pg

# Boxes have position (bottom right corner) and size (length and height)

class Box(object):
    def __init__(self,posx,posy,length,height,r=255,g=255,b=255,alpha=255):
        self.posx_ = posx
        self.posy_ = posy
        self.length_ = length
        self.height_ = height

        verts = (self.posx_,self.posy_, self.posx_+self.length_,self.posy_, self.posx_+self.length_,self.posy_+self.height_, self.posx_,self.posy_+self.height_)
        self.rgba_ = (r, g, b, alpha)

        self.vert_list_ = pg.graphics.vertex_list(4, 
            ('v2f', verts),
            ('c4B', self.rgba_ + self.rgba_ + self.rgba_ + self.rgba_)  #Color for each vertice
        )

    def draw(self):
        self.vert_list_.draw(pg.gl.GL_POLYGON)

    def getPosX(self):
        return self.posx_
    def getPosY(self):
        return self.posy_
    def getLength(self):
        return self.length_
    def getHeight(self):
        return self.height_

    def setPos(self,posx,posy):
        self.posx_ = posx
        self.posy_ = posy
        verts = self.getVerts()
        self.vert_list_.vertices  = verts
    def setSize(self,length,height,centered=False):
        deltaposx = (length-self.length_)/2
        deltaposy = (height-self.height_)/2
        self.length_ = length
        self.height_ = height
        if centered == True:
            self.posx_ = self.posx_ - deltaposx
            self.posy_ = self.posy_ - deltaposy
        verts = self.getVerts()
        self.vert_list_.vertices = verts
    def move(self,dx,dy):
        self.posx_ = self.posx_ + dx
        self.posy_ = self.posy_ + dy
        verts = self.getVerts()
        self.vert_list_.vertices = verts
    def scale(self,lScale,hScale,centered=False):
        deltaposx = (self.length_*lScale - self.length_)/2
        deltaposy = (self.height_*hScale - self.height_)/2
        self.length_ = self.length_*lScale
        self.height_ = self.height_*hScale
        if centered == True:
            self.posx_ = self.posx_ - deltaposx
            self.posy_ = self.posy_ - deltaposy
        
        verts = self.getVerts()
        self.vert_list_.vertices = verts
    
    def setColor(self,r,g,b,alpha):
        rgba = [r, g, b, alpha]
        self.vert_list_.colors = rgba + rgba + rgba + rgba
    
    def outOfBounds(self, xbound, ybound):
        if self.posx_ + self.length_ > xbound or self.posx_ < 0:
            return "x"
        if self.posy_ + self.height_ > ybound or self.posy_ < 0:
            return "y"
        else:
            return "none"
    def getVerts(self):
        return [self.posx_,self.posy_, self.posx_+self.length_,self.posy_, self.posx_+self.length_,self.posy_+self.height_, self.posx_,self.posy_+self.height_]

# Circles have a fixed radius, and ideally an infinite number of vertices. However,
# we can't actually draw an infinite number of vertices, so we have to approximate. 
# Approximating requires a number of vertices N separated by some constant angle, and
# this can be computationally expensive if we're not careful. A rotation matrix will
# used to calculate the position of the vertices, thus eliminating many expensive sine/cosine
# functions.

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
    
# Lines have two coordinates, a start and an end, and a width in pixels

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
            ('v2f',self.getHeadVerts_()),
            ('c4B',self.rgba_ + self.rgba_ + self.rgba_)
        )
    
    def draw(self):
        pg.gl.glLineWidth(self.width_)
        self.vert_list_.draw(pg.gl.GL_LINES)
        self.arrowhead_.draw(pg.gl.GL_POLYGON)
    
    def setPosA(self,x,y):
        self.verts_ = (x,y) + self.verts_[2:4]
        self.vert_list_.vertices = self.verts_
        self.arrowhead_.vertices = self.getHeadVerts_()
    def setPosB(self,x,y):
        self.angle_ = self.getAngle()
        x = x - self.width_*math.cos(self.angle_)
        y = y - self.width_*math.sin(self.angle_)
        self.verts_ = self.verts_[0:2] + (x,y)
        self.vert_list_.vertices = self.verts_
        self.arrowhead_.vertices = self.getHeadVerts_()
    def setPos(self,x1,y1,x2,y2):
        self.angle_ = self.getAngle()
        x2 = x2 - self.width_*math.cos(self.angle_)
        y2 = y2 - self.width_*math.sin(self.angle_)
        self.verts_ = (x1,y1, x2,y2)
        self.vert_list_.vertices = self.verts_
        self.arrowhead_.vertices = self.getHeadVerts_()
    def setColor(self,r,g,b,alpha):
        rgba = (r,g,b,alpha)
        self.vert_list_.colors = rgba + rgba

    def getHeadVerts_(self):
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


class Text(object):
    def __init__(self,text,posx,posy,
                fontname='Times New Roman',fontsize=20,
                anchorx='left',anchory='center',
                rgba = (255,255,255,255),bold=False,italic=False,
                multiline=False,width=None):
        self.text_ = text
        self.fontname_ = fontname
        self.fontsize_ = fontsize
        self.posx_ = posx
        self.posy_ = posy
        self.anchorx_ = anchorx
        self.anchory_ = anchory
        self.rgba_ = rgba
        self.bold_ = bold
        self.italic_ = italic
        self.multiline_ = multiline
        self.width_ = width

        self.label_ = pg.text.Label(self.text_,font_name=self.fontname_,
                                    font_size=self.fontsize_,
                                    x=self.posx_,y=self.posy_,
                                    anchor_x=self.anchorx_,anchor_y=self.anchory_,
                                    color=self.rgba_,bold=self.bold_,italic=self.italic_,
                                    multiline=self.multiline_,width=self.width_)
    def draw(self):
        self.label_.draw()

    def getPosX(self):
        return self.posx_
    def getPosY(self):
        return self.posy_
    def getFontSize(self):
        return self.fontsize_
    def getFontName(self):
        return self.fontname_
    def getAnchorX(self):
        return self.anchorx_
    def getAnchorY(self):
        return self.anchory_

    def setPos(self,posx,posy):
        self.posx_ = posx
        self.posy_ = posy
        self.label_.x = self.posx_
        self.label_.y = self.posy_
    def setSize(self,fontsize):
        self.fontsize_ = fontsize
        self.label.font_size = self.fontsize_
    def move(self,dx,dy):
        self.posx_ = self.posx_ + dx
        self.posy_ = self.posy_ + dy
        self.label_.x = self.posx_
        self.label_.y = self.posy_
    def scale(self,scalefactor):
        self.fontsize_ = self.fontsize_ * scalefactor
        self.label_.font_size = self.fontsize_
    def setAnchorX(self,anchorx):
        self.anchorx_ = anchorx
        self.label_.anchor_x = self.anchorx_
    def setAnchorY(self,anchory):
        self.anchory_ = anchory
        self.label_.anchor_y = self.anchory_
    def setColor(self,rgba):
        self.rgba_ = rgba
        self.label_.color = self.rgba_
    def setMultiline(self,multiline):
        self.multiline_ = multiline
        self.label_.multiline = self.multiline_
    def setWidth(self,width):
        if self.multiline_ == True:
            self.width_ = width
            self.label_.width = self.width_

