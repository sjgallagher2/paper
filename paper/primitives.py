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
        self.rgba_ = [r, g, b, alpha]
        rgba = [math.floor(r), math.floor(g), math.floor(b), math.floor(alpha)] #Only use floors but store fractional parts too

        self.vert_list_ = pg.graphics.vertex_list(4, 
            ('v2f', verts),
            ('c4B', rgba + rgba + rgba + rgba)  #Color for each vertice
        )
        self.visible_ = True

    def draw(self):
        if self.visible_ == True:
            self.vert_list_.draw(pg.gl.GL_POLYGON)

    def getPosX(self):
        return self.posx_
    def getPosY(self):
        return self.posy_
    def getLength(self):
        return self.length_
    def getHeight(self):
        return self.height_
    def getColor(self):
        return self.rgba_

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
        self.rgba_ = [r,g,b,alpha] #Store absolute (including fractional) values for color
        #Only use the floors to set the vertex color
        rgba = [math.floor(r), math.floor(g), math.floor(b), math.floor(alpha)]
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
    def setVisible(self,visible=True):
        if visible == False:
            self.visible_ = False
        else:
            self.visible_ = True
    def popUpState(self,t,tpop,length,height,intensity=0.3,damping=3):
        """
        @brief
        Box popup animation for use in a state machine
        
        @param
        t         Elapsed time (seconds) for popup, starting at 0
        tpop      Time to stop the box pop animation (hard stop)
        length    Final box length
        height    Final box height
        intensity   Controls amplitude of popping/bouncing (optional)
        damping     Controls duration of popping/bouncing (optional)
        
        @return
        1         Animation continues
        -1        Animation complete
        
        Use this in a state machine by storing the elapsed time, and changing
        state only when -1 is returned
        """
        scalefactor = 1 + intensity*math.exp(-damping*t)*math.sin(15*t)
        if t < tpop:
            self.setSize(length*scalefactor,height*scalefactor,centered=True)
            return 1 #Animation continues
        else:
            self.setSize(length,height,centered=True)
            return -1 #Animation complete
    def fadeState(self,t,dt,tfade,bgcolor,objcolor,direction):
        """
        @brief
        Fade in or out animation for primitives for use in a state machine

        @param
        t           Elapsed time (seconds) starting at 0 (update every call)
        dt          Time (seconds) since last update
        tfade       Time (seconds) for the fade in (constant through animation)
        bgcolor     Color of background in RGBA list (integers between 0 and 255)
        objcolor    Final color of object in RGBA list (integers between 0 and 255)
        direction   Direction of fade, "in" or "out"

        @returns
        1           Animation continues
        -1          Animation complete
        """
        #First time steps, reset object color
        if t == 0 or t == dt:
            if direction == "in":
                self.setColor(bgcolor[0],bgcolor[1],bgcolor[2],bgcolor[3])
            elif direction == "out":
                self.setColor(objcolor[0],objcolor[1],objcolor[2],objcolor[3])
        if direction == "in":
            redrate = (objcolor[0]-bgcolor[0])/tfade    #These should remain constant through the animation
            greenrate = (objcolor[1]-bgcolor[1])/tfade 
            bluerate = (objcolor[2]-bgcolor[2])/tfade 
        elif direction == "out":
            redrate = (bgcolor[0]-objcolor[0])/tfade    #These should remain constant through the animation
            greenrate = (bgcolor[1]-objcolor[1])/tfade 
            bluerate = (bgcolor[2]-objcolor[2])/tfade 
        r = self.getColor()[0]
        g = self.getColor()[1]
        b = self.getColor()[2]

        if t < tfade:
            #Change color
            dr = redrate*dt
            dg = greenrate*dt
            db = bluerate*dt
            self.setColor(r+dr, g+dg, b+db, 255)
            return 1
        else:
            if direction == "in":
                self.setColor(objcolor[0],objcolor[1],objcolor[2],objcolor[3])
            elif direction == "out":
                self.setColor(bgcolor[0],bgcolor[1],bgcolor[2],bgcolor[3])

            return -1



# Circles have a fixed radius, and ideally an infinite number of vertices. However,
# we can't actually draw an infinite number of vertices, so we have to approximate. 
# Approximating requires a number of vertices N separated by some constant angle, and
# this can be computationally expensive if we're not careful. A rotation matrix is
# used to calculate the position of the vertices, thus eliminating many expensive sine/cosine
# functions.

class Circle(object):
    def __init__(self, posx,posy,rad,N=30,r=255,g=255,b=255,alpha=255):
        self.posx_ = posx
        self.posy_ = posy
        self.rad_ = rad
        self.nVerts_ = N
        self.rgba_ = [r, g, b, alpha]
        self.visible_ = True

        self.theta_ = 2*math.pi/self.nVerts_
        self.cosTheta_ = math.cos(self.theta_)
        self.sinTheta_ = math.sin(self.theta_)

        self.verts_ = self.getVerts_()

        self.vert_list_ = pg.graphics.vertex_list(self.nVerts_,
            ('v2f',self.verts_),
            ('c4B',self.getColors_())
        )

    def draw(self):
        if self.visible_ == True:
            self.vert_list_.draw(pg.gl.GL_POLYGON)
    
    def getPosX(self):
        return self.posx_
    def getPosY(self):
        return self.posy_
    def getRadius(self):
        return self.rad_
    def getNVerts(self):
        return self.nVerts_
    def getColor(self):
        return self.rgba_
    
    def move(self,dx,dy):
        self.posx_ = self.posx_ + dx
        self.posy_ = self.posy_ + dy
        for i in range(0,self.nVerts_*2,2):
            self.verts_[i] = self.verts_[i] + dx
            self.verts_[i+1] = self.verts_[i+1] + dy
        self.vert_list_.vertices = self.verts_
    def setPos(self,posx,posy):
        deltax = posx - self.posx_
        deltay = posy - self.posy_
        self.move(deltax,deltay)
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
    def setColor(self,r,g,b,alpha=255):
        self.rgba_ = [r,g,b,alpha]
        self.vert_list_.colors = self.getColors_()
    def setVisible(self,visible=True):
        if visible == False:
            self.visible_ = False
        else:
            self.visible_ = True

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
        rgba = [math.floor(self.rgba_[0]),math.floor(self.rgba_[1]),math.floor(self.rgba_[2]),math.floor(self.rgba_[3])]
        for i in range(1,self.nVerts_):
            rgba = rgba + self.rgba_
        return rgba

    def fadeState(self,t,dt,tfade,bgcolor,objcolor,direction):
        """
        @brief
        Fade in or out animation for primitives for use in a state machine

        @param
        t           Elapsed time (seconds) starting at 0 (update every call)
        dt          Time (seconds) since last update
        tfade       Time (seconds) for the fade in (constant through animation)
        bgcolor     Color of background in RGBA list (integers between 0 and 255)
        objcolor    Final color of object in RGBA list (integers between 0 and 255)
        direction   Direction of fade, "in" or "out"

        @returns
        1           Animation continues
        -1          Animation complete
        """
        #First time steps, reset object color
        if t == 0 or t == dt:
            if direction == "in":
                self.setColor(bgcolor[0],bgcolor[1],bgcolor[2],bgcolor[3])
            elif direction == "out":
                self.setColor(objcolor[0],objcolor[1],objcolor[2],objcolor[3])
        if direction == "in":
            redrate = (objcolor[0]-bgcolor[0])/tfade    #These should remain constant through the animation
            greenrate = (objcolor[1]-bgcolor[1])/tfade 
            bluerate = (objcolor[2]-bgcolor[2])/tfade 
        elif direction == "out":
            redrate = (bgcolor[0]-objcolor[0])/tfade    #These should remain constant through the animation
            greenrate = (bgcolor[1]-objcolor[1])/tfade 
            bluerate = (bgcolor[2]-objcolor[2])/tfade 
        r = self.getColor()[0]
        g = self.getColor()[1]
        b = self.getColor()[2]

        if t < tfade:
            #Change color
            dr = redrate*dt
            dg = greenrate*dt
            db = bluerate*dt
            self.setColor(r+dr, g+dg, b+db, 255)
            return 1
        else:
            if direction == "in":
                self.setColor(objcolor[0],objcolor[1],objcolor[2],objcolor[3])
            elif direction == "out":
                self.setColor(bgcolor[0],bgcolor[1],bgcolor[2],bgcolor[3])

            return -1
    def popUpState(self,t,tpop,radius,intensity=0.3,damping=3):
        """
        @brief
        Circle popup animation for use in a state machine
        
        @param
        t           Elapsed time (seconds) for popup, starting at 0
        tpop        Time to stop animation (hard stop)
        radius      Final radius of circle
        intensity   Controls amplitude of popping/bouncing (optional)
        damping     Controls duration of popping/bouncing (optional)
        
        @return
        1           Animation continues
        -1          Animation complete
        
        Use this in a state machine by storing the elapsed time, and changing
        state only when -1 is returned
        """
        scalefactor = 1 + intensity*math.exp(-damping*t)*math.sin(15*t)
        if t < tpop:
            self.setRadius(radius*scalefactor)
            return 1 #Animation continues
        else:
            self.setRadius(radius)
            return -1 #Animation complete
    
# Lines have two coordinates, a start and an end, and a width in pixels

class Line(object):
    def __init__(self, x1,y1, x2,y2, width=1, r=255,g=255,b=255,alpha=255):
        self.verts_ = (x1,y1, x2,y2)
        self.width_ = width
        self.rgba_ = (r, g, b, alpha)
        self.visible_ = True
        rgba = [math.floor(self.rgba_[0]),math.floor(self.rgba_[1]),math.floor(self.rgba_[2]),math.floor(self.rgba_[3])]
        self.vert_list_ = pg.graphics.vertex_list(2,
            ('v2f',self.verts_),
            ('c4B', rgba + rgba)
        )
    def draw(self):
        if self.visible_ == True:
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
        arg = math.atan2(deltay,deltax)
        return arg
    def getColor(self):
        return self.rgba_
    
    def setPosA(self,x,y):
        self.verts_ = (x,y) + self.verts_[2:4]
        self.vert_list_.vertices = self.verts_
    def setPosB(self,x,y):
        self.verts_ = self.verts_[0:2] + (x,y)
        self.vert_list_.vertices = self.verts_
    def setPos(self,x1,y1,x2,y2):
        self.verts_ = (x1,y1, x2,y2)
        self.vert_list_.vertices = self.verts_
    def scaleLength(self,scalefactor):
        length = scalefactor*self.getLength()
        angle = self.getAngle()
        x = length*math.cos(angle) + self.verts_[0]
        y = length*math.sin(angle) + self.verts_[1]
        self.verts_ = self.verts_[0:2] + (x,y)
        self.vert_list_.vertices = self.verts_
    def setLength(self,length):
        angle = self.getAngle()
        x = length*math.cos(angle) + self.verts_[0]
        y = length*math.sin(angle) + self.verts_[1]
        self.verts_ = self.verts_[0:2] + (x,y)
        self.vert_list_.vertices = self.verts_
    def setAngle(self,angle):
        length = self.getLength()
        x = length*math.cos(angle) + self.verts_[0]
        y = length*math.sin(angle) + self.verts_[1]
        self.verts_ = self.verts_[0:2] + (x,y)
        self.vert_list_.vertices = self.verts_
    def setDirection(self,x,y):
        #Set angle so that the arrow points to (x,y)
        angle = math.atan2(y-self.verts_[1],x-self.verts_[0])
        self.setAngle(angle)
    def rotate(self,angle):
        angle = angle + self.getAngle()
        self.setAngle(angle)
    def setColor(self,r,g,b,alpha):
        self.rgba_ = [r,g,b,alpha]
        rgba = [math.floor(self.rgba_[0]),math.floor(self.rgba_[1]),math.floor(self.rgba_[2]),math.floor(self.rgba_[3])]
        self.vert_list_.colors = rgba + rgba
    def setVisible(self,visible=True):
        if visible == False:
            self.visible_ = False
        else:
            self.visible_ = True
    def setWidth(self,w):
        self.width_ = w
    def fadeState(self,t,dt,tfade,bgcolor,objcolor,direction):
        """
        @brief
        Fade in or out animation for primitives for use in a state machine

        @param
        t           Elapsed time (seconds) starting at 0 (update every call)
        dt          Time (seconds) since last update
        tfade       Time (seconds) for the fade in (constant through animation)
        bgcolor     Color of background in RGBA list (integers between 0 and 255)
        objcolor    Final color of object in RGBA list (integers between 0 and 255)
        direction   Direction of fade, "in" or "out"

        @returns
        1           Animation continues
        -1          Animation complete
        """
        #First time steps, reset object color
        if t == 0 or t == dt:
            if direction == "in":
                self.setColor(bgcolor[0],bgcolor[1],bgcolor[2],bgcolor[3])
            elif direction == "out":
                self.setColor(objcolor[0],objcolor[1],objcolor[2],objcolor[3])
        if direction == "in":
            redrate = (objcolor[0]-bgcolor[0])/tfade    #These should remain constant through the animation
            greenrate = (objcolor[1]-bgcolor[1])/tfade 
            bluerate = (objcolor[2]-bgcolor[2])/tfade 
        elif direction == "out":
            redrate = (bgcolor[0]-objcolor[0])/tfade    #These should remain constant through the animation
            greenrate = (bgcolor[1]-objcolor[1])/tfade 
            bluerate = (bgcolor[2]-objcolor[2])/tfade 
        r = self.getColor()[0]
        g = self.getColor()[1]
        b = self.getColor()[2]

        if t < tfade:
            #Change color
            dr = redrate*dt
            dg = greenrate*dt
            db = bluerate*dt
            self.setColor(r+dr, g+dg, b+db, 255)
            return 1
        else:
            if direction == "in":
                self.setColor(objcolor[0],objcolor[1],objcolor[2],objcolor[3])
            elif direction == "out":
                self.setColor(bgcolor[0],bgcolor[1],bgcolor[2],bgcolor[3])

            return -1
    def extendState(self,t,dt,textend,x,y):
        """
        @brief
        Line extending animation state for state machine

        @params
        t       Elapsed time for animation (starting at 0)
        dt      Time since last update
        textend Time to stop extending
        x       Final position x to point to (absolute)
        y       Final position y to point to (absolute)
        
        @return
        1       Animation continues
        -1      Animation finished
        """
        deltaLength = math.sqrt(math.pow(x - self.verts_[0],2)+math.pow(y - self.verts_[1],2))
        lengthRate = deltaLength/textend
        if t == 0 or t == dt:
            self.setLength(5)
            self.setDirection(x,y)

        if t < textend:
            self.setLength(self.getLength() + lengthRate*dt)
            self.setDirection(x,y)
            return 1
        else:
            self.setPosB(x,y)
            return -1
            


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
        
        rgba = [math.floor(self.rgba_[0]),math.floor(self.rgba_[1]),math.floor(self.rgba_[2]),math.floor(self.rgba_[3])]
        self.visible_ = True
        
        #Adjust for arrowhead by reducing length
        angle = self.getAngle()
        Line.setPosB(self,x2 - self.width_*math.cos(angle), 
                    y2 - self.width_*math.sin(angle))
        
        #Create arrowhead
        self.arrowhead_ = pg.graphics.vertex_list(3,
            ('v2f',self.getHeadVerts_()),
            ('c4B',rgba + rgba + rgba)
        )
    
    def draw(self):
        if self.visible_ == True:
            pg.gl.glLineWidth(self.width_)
            self.vert_list_.draw(pg.gl.GL_LINES)
            self.arrowhead_.draw(pg.gl.GL_POLYGON)
    
    def getLength(self):
        deltax = self.verts_[2] - self.verts_[0]
        deltay = self.verts_[3] - self.verts_[1]
        norm = math.sqrt(math.pow(deltax,2) + math.pow(deltay,2)) + self.width_
        return norm
    
    def setPosA(self,x,y):
        self.verts_ = (x,y) + self.verts_[2:4]
        self.vert_list_.vertices = self.verts_
        self.arrowhead_.vertices = self.getHeadVerts_()
    def setPosB(self,x,y):
        self.angle_ = self.getAngle()
        x = x - self.width_*math.cos(self.angle_) #Correction for width to get pointed tip
        y = y - self.width_*math.sin(self.angle_)
        self.verts_ = self.verts_[0:2] + (x,y)
        self.vert_list_.vertices = self.verts_
        self.arrowhead_.vertices = self.getHeadVerts_()
    def setPos(self,x1,y1,x2,y2):
        self.angle_ = self.getAngle()
        x2 = x2 - self.width_*math.cos(self.angle_) #Correction for width to get pointed tip
        y2 = y2 - self.width_*math.sin(self.angle_)
        self.verts_ = (x1,y1, x2,y2)
        self.vert_list_.vertices = self.verts_
        self.arrowhead_.vertices = self.getHeadVerts_()
    def scaleLength(self,scalefactor):
        length = scalefactor*self.getLength() - self.width_
        angle = self.getAngle()
        x = length*math.cos(angle) + self.verts_[0]
        y = length*math.sin(angle) + self.verts_[1]
        self.verts_ = self.verts_[0:2] + (x,y)
        self.vert_list_.vertices = self.verts_
        self.arrowhead_.vertices = self.getHeadVerts_()
    def setLength(self,length):
        angle = self.getAngle()
        length = length-self.width_
        x = length*math.cos(angle) + self.verts_[0]
        y = length*math.sin(angle) + self.verts_[1]
        self.verts_ = self.verts_[0:2] + (x,y)
        self.vert_list_.vertices = self.verts_
        self.arrowhead_.vertices = self.getHeadVerts_()
    def setAngle(self,angle):
        length = self.getLength() - self.width_
        x = length*math.cos(angle) + self.verts_[0]
        y = length*math.sin(angle) + self.verts_[1]
        self.verts_ = self.verts_[0:2] + (x,y)
        self.vert_list_.vertices = self.verts_
        self.arrowhead_.vertices = self.getHeadVerts_()
    def setDirection(self,x,y,absolute=False):
        #Set angle so that the arrow points to (x,y)
        if absolute == False:
            #Set direction relative to position
            angle = math.atan2(y-self.verts_[1],x-self.verts_[0])
        else:
            #Set direction relative to (0,0)
            angle = math.atan2(y,x)
        self.setAngle(angle)
    def rotate(self,angle):
        angle = angle + self.getAngle()
        self.setAngle(angle)
    def setColor(self,r,g,b,alpha):
        self.rgba_ = [r,g,b,alpha]
        rgba = [math.floor(self.rgba_[0]),math.floor(self.rgba_[1]),math.floor(self.rgba_[2]),math.floor(self.rgba_[3])]
        self.vert_list_.colors = rgba + rgba
        self.arrowhead_.colors = rgba + rgba + rgba
    def setVisible(self,visible=True):
        if visible == False:
            self.visible_ = False
        else:
            self.visible_ = True

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
                fontname='Futura',fontsize=20,
                anchorx='left',anchory='center',
                rgba = [255,255,255,255],bold=False,italic=False,
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
        self.visible_ = True

        rgba = [math.floor(self.rgba_[0]),math.floor(self.rgba_[1]),math.floor(self.rgba_[2]),math.floor(self.rgba_[3])]

        self.label_ = pg.text.Label(self.text_,font_name=self.fontname_,
                                    font_size=self.fontsize_,
                                    x=self.posx_,y=self.posy_,
                                    anchor_x=self.anchorx_,anchor_y=self.anchory_,
                                    color=rgba,bold=self.bold_,italic=self.italic_,
                                    multiline=self.multiline_,width=self.width_)
    def draw(self):
        if self.visible_ == True:
            self.label_.draw()

    def getText(self):
        return self.text_
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
    def getColor(self):
        return self.rgba_

    def setText(self,text):
        self.text_ = text
        self.label_.text = self.text_
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
        rgba = [math.floor(self.rgba_[0]),math.floor(self.rgba_[1]),math.floor(self.rgba_[2]),math.floor(self.rgba_[3])]
        self.label_.color = rgba
    def setVisible(self,visible=True):
        if visible == False:
            self.visible_ = False
        else:
            self.visible_ = True
    def setMultiline(self,multiline):
        self.multiline_ = multiline
        self.label_.multiline = self.multiline_
    def setWidth(self,width):
        if self.multiline_ == True:
            self.width_ = width
            self.label_.width = self.width_
    def fadeState(self,t,dt,tfade,bgcolor,objcolor,direction):
        """
        @brief
        Fade in or out animation for primitives for use in a state machine

        @param
        t           Elapsed time (seconds) starting at 0 (update every call)
        dt          Time (seconds) since last update
        tfade       Time (seconds) for the fade in (constant through animation)
        bgcolor     Color of background in RGBA list (integers between 0 and 255)
        objcolor    Final color of object in RGBA list (integers between 0 and 255)
        direction   Direction of fade, "in" or "out"

        @returns
        1           Animation continues
        -1          Animation complete
        """
        #First time steps, reset object color
        if t == 0 or t == dt:
            if direction == "in":
                self.setColor(bgcolor[0],bgcolor[1],bgcolor[2],bgcolor[3])
            elif direction == "out":
                self.setColor(objcolor[0],objcolor[1],objcolor[2],objcolor[3])
        if direction == "in":
            redrate = (objcolor[0]-bgcolor[0])/tfade    #These should remain constant through the animation
            greenrate = (objcolor[1]-bgcolor[1])/tfade 
            bluerate = (objcolor[2]-bgcolor[2])/tfade 
        elif direction == "out":
            redrate = (bgcolor[0]-objcolor[0])/tfade    #These should remain constant through the animation
            greenrate = (bgcolor[1]-objcolor[1])/tfade 
            bluerate = (bgcolor[2]-objcolor[2])/tfade 
        r = self.getColor()[0]
        g = self.getColor()[1]
        b = self.getColor()[2]

        if t < tfade:
            #Change color
            dr = redrate*dt
            dg = greenrate*dt
            db = bluerate*dt
            self.setColor(r+dr, g+dg, b+db, 255)
            return 1
        else:
            if direction == "in":
                self.setColor(objcolor[0],objcolor[1],objcolor[2],objcolor[3])
            elif direction == "out":
                self.setColor(bgcolor[0],bgcolor[1],bgcolor[2],bgcolor[3])

            return -1
    def popUpState(self,t,tpop,fontsize,intensity=0.3,damping=3):
        """
        @brief
        Text popup animation for use in a state machine
        
        @param
        t           Elapsed time (seconds) for popup, starting at 0
        tpop        Time to stop animation (hard stop)
        radius      Final radius of circle
        intensity   Controls amplitude of popping/bouncing (optional)
        damping     Controls duration of popping/bouncing (optional)
        
        @return
        1           Animation continues
        -1          Animation complete
        
        Use this in a state machine by storing the elapsed time, and changing
        state only when -1 is returned
        """
        scalefactor = 1 + intensity*math.exp(-damping*t)*math.sin(15*t)
        if t < tpop:
            self.setSize(fontsize*scalefactor)
            return 1 #Animation continues
        else:
            self.setSize(fontsize)
            return -1 #Animation complete



