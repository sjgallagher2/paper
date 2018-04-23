# widget.py
# Sam Gallagher
# 12 April 2018
#
# A type of scene which serves a repeatable function. Widgets are scenes, the only
# difference is the context you use them in. Any scene can be used as a widget, but
# you should subclass widgets instead for better organization.

from paper.core import Scene
from paper.primitives import Box

class Widget(Scene):
    def __init__(self,winsz,posx,posy):
        Scene.__init__(self,winsz)
        self.posx_ = posx
        self.posy_ = posy

        #Initialize objects
        self.objects = {}   #A dictionary
    def draw(self):
        #Draw objects in ALPHABETICAL ORDER (numbered keys recommended)
        for name,obj in sorted(self.objects.items()):
            obj.draw()
    def update(self,dt):
        #Update based on input params
        pass
    def getPosX(self):
        return self.posx_
    def getPosY(self):
        return self.posy_
    def getPos(self):
        pos = [self.posx_, self.posy_]
    
    def setPosX(self,posx):
        deltax = posx-self.posx_
        self.posx_ = posx
        for name,obj in self.objects.items():
            obj.move(deltax,0)
    def setPosY(self,posy):
        deltay = posy-self.posy_
        self.posy_ = posy
        for name,obj in self.objects.items():
            obj.move(0,deltay)
    def setPos(self,posx,posy):
        deltax = posx-self.posx_
        deltay = posy-self.posy_
        self.posx_ = posx
        self.posy_ = posy
        for name,obj in self.objects.items():
            obj.move(deltax,deltay)
    def move(self,dx,dy):
        for name,obj in self.objects.items():
            obj.move(dx,dy)
    def setVisible(self,visible=False):
        if visible == False:
            for _,obj in self.objects.items():
                obj.setVisible(False)
        else:
            for _,obj in self.objects.items():
                obj.setVisible(True)



class LoadingBar(Widget):
    def __init__(self,winsz,posx,posy,height, barcolor = [0,255,0]):
        Widget.__init__(self,winsz,posx,posy)
        self.height_ = height
        self.width_ = 0.16*self.height_
        self.barr_ = barcolor[0]
        self.barg_ = barcolor[1]
        self.barb_ = barcolor[2]

        #Initialize objects
        self.objects["0.outline"] = Box(self.posx_,self.posy_, self.width_,self.height_)
        self.objects["1.emptybar"] = Box(self.posx_+self.width_/4,self.posy_+self.width_/4, 
                            self.width_/2,self.height_-self.width_/2, 
                            r=0,g=0,b=0)
        self.objects["2.progress"] = Box(self.posx_+self.width_/4,self.posy_+self.width_/4,
                            self.width_/2,self.height_-self.width_/2, 
                            r=self.barr_,g=self.barg_,b=self.barb_)
    
    def setProgress(self, prog):
        self.objects["2.progress"].setSize(self.objects["2.progress"].getLength(), self.objects["1.emptybar"].getHeight()*(prog/100.0))
    def setBarColor(self, r,g,b,alpha=255):
        self.barr_ = r
        self.barg_ = g
        self.barb_ = b
        self.objects["2.progress"].setColor(r,g,b,alpha)

