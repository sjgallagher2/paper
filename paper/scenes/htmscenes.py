# Animation object for an HTM column
import math
from paper.core import Scene
from paper.primitives import Box,Circle,Text
from paper.widget import Widget,LoadingBar

class HTMColumn(Widget):
    def __init__(self,winsz,posx,posy,ncells):
        Widget.__init__(self,winsz,posx,posy)
        
        self.width_ = 50
        self.height_ = 200
        self.ncells_ = 6
        self.cellrad_ = (self.width_*0.5)/2 #Cell takes up 50% of column width
        self.deltat = 0.0
        self.objects["0.outline"] = Box(self.posx_,self.posy_, self.width_,self.height_) #White outline box
        cellspacing = self.height_/(self.ncells_+1)
        for i in range(1,self.ncells_+1):
            self.objects[str(i)+".Cell" + str(i)] = Circle(self.posx_+self.width_/2,self.posy_+(i)*cellspacing,self.cellrad_,
                                r=200,g=200,b=200)
    
    def getActiveCells(self):
        activelist = []
        for name,obj in self.objects.items():
            if "Cell" in name:
                if obj.getColor() == [255,50,50,255]:
                    activelist.append( self.getCellNumber_(name) )
        return activelist
    def getNCells(self):
        return self.ncells_

    def setActiveCells(self,activelist): 
        for name,obj in self.objects.items():  #Reset cell colors
            if "Cell" in name:
                obj.setColor(200,200,200)
                if self.getCellNumber_(name) in activelist:
                    obj.setColor(255,50,50)
    
    def setCellPos_(self):
        for name,obj in self.objects.items():
            if "Cell" in name:
                i = self.getCellNumber_(name)
                posx = self.posx_ + self.width_/2
                posy = self.posy_ + i*cellspacing
                obj.setPos( posx,posy )
    def getCellNumber_(self,name):
        if "Cell" in name:
            cellnum = name[ (name.find("Cell")+4) : ]
            return int(cellnum)
        else:
            return -1



class ColumnTestScene(Scene):
    def __init__(self,winsz):
        Scene.__init__(self,winsz)
        self.col1 = HTMColumn(winsz,100,100,3)
    
    def draw(self):
        self.col1.draw()
    
    def update(self,dt):
        self.deltat = self.deltat + dt
        self.col1.update(dt)
        if math.floor(self.deltat)%2 == 0:
            self.col1.setActiveCells([1,3])
        else:
            self.col1.setActiveCells([])

