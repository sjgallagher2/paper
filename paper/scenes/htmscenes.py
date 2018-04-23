# Animation object for an HTM column
import math
import random
from paper.core import Scene
from paper.primitives import Box,Circle,Text,Arrow
from paper.widget import Widget,LoadingBar

class HTMColumn(Widget):
    def __init__(self,winsz,posx,posy,ncells):
        Widget.__init__(self,winsz,posx,posy)
        
        self.width_ = 50
        self.height_ = 200
        self.ncells_ = 6
        self.cellrad_ = (self.width_*0.5)/2 #Cell takes up 50% of column width
        self.deltat = 0.0
        self.outlineWidth = 2
        self.objects["0.outline"] = Box(self.posx_-self.outlineWidth,self.posy_-self.outlineWidth, 
                                        self.width_ + 2*self.outlineWidth,self.height_ + 2*self.outlineWidth,
                                        r=0,g=0,b=0,alpha=255) #red outline box
        self.objects["1.background"] = Box(self.posx_,self.posy_, self.width_,self.height_) #White background box
        cellspacing = self.height_/(self.ncells_+1)
        for i in range(1,self.ncells_+1):
            self.objects[str(i+1)+".Cell" + str(i)] = Circle(self.posx_+self.width_/2,self.posy_+(i)*cellspacing,self.cellrad_,
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
    def getCellPos(self,cellid):
        for name,obj in self.objects.items():
            if "Cell" in name:
                if self.getCellNumber_(name) == cellid:
                    return [obj.getPosX(),obj.getPosY()]
        return []
    def getColPos(self,side="top"):
        #Get position on the edge of the column in the middle of the edge
        if side == "top":
            return [self.posx_ + self.width_/2, self.posy_ + self.height_]
        elif side == "bottom":
            return [self.posx_ + self.width_/2, self.posy_]
        elif side == "left":
            return [self.posx_, self.posy_ + self.height_/2]
        elif side == "right":
            return [self.posx_ + self.width_, self.posy_ + self.height/2]

    def setOutline(self,outline = True):
        if outline == True:
            self.objects["0.outline"].setColor(255,0,0,255)
        else:
            self.objects["0.outline"].setColor(0,0,0,255)
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

class BitElement(Widget):
    def __init__(self,winsz,posx,posy,height,width,borderwidth=2):
        Widget.__init__(self,winsz,posx,posy)
        self.posx_ = posx
        self.posy_ = posy
        self.height_ = height
        self.width_ = width
        self.fontsize_ = self.height_/2
        self.borderthickness_ = borderwidth
        self.objects["0.outline"] = Box(self.posx_-self.borderthickness_,self.posy_-self.borderthickness_,
                                        self.width_+self.borderthickness_*2,self.height_+self.borderthickness_*2,r=90,g=90,b=90)
        self.objects["1.bg"] = Box(self.posx_,self.posy_,self.width_,self.height_)
        self.objects["2.bit"] = Text("0",self.posx_+ self.width_/2 - self.fontsize_/2,self.posy_+self.fontsize_, rgba=[0,0,0,255],fontsize=self.fontsize_)
    
    def getBitValue(self):
        return int(self.objects["2.bit"].getText())

    def randomInput(self):
        random.seed()
        r = random.randint(0,1)
        self.objects["2.bit"].setText(str(r))
    def shadeBit(self,active=True,connected=True):
        if active == True:
            if connected == True:
                # Active and connected synapse
                self.objects["1.bg"].setColor(r=155,g=250,b=155,alpha=255)
            else:
                # Active but no connected synapse
                self.objects["1.bg"].setColor(r=255,g=255,b=0,alpha=255)
        else:
            if connected == True:
                # Connected but not active
                self.objects["1.bg"].setColor(r=255,g=155,b=155,alpha=255)
            else:
                # Not connected, not active
                self.objects["1.bg"].setColor(r=255,g=255,b=255,alpha=255)
    

class InputSpace(Widget):
    def __init__(self,winsz,posx,posy,spacesize):
        Widget.__init__(self,winsz,posx,posy)
        self.nspaces_ = spacesize
        self.height_ = 30
        self.spacewidth_ = 30
        self.length_ = self.nspaces_*self.spacewidth_
        self.objects["00.outline"] = Box(self.posx_,self.posy_,self.length_,self.height_)
        self.deltat = 0.0
        
        for i in range(1,self.nspaces_+1):  #Range() is exclusive on the upper limit
            if i < 10:
                key = "0" + str(i) + ".bit" + str(i)
            elif i < 100:
                key = str(i) + ".bit" + str(i)
            self.objects[key] = BitElement(winsz,self.posx_+self.spacewidth_*(i-1),self.posy_,self.height_,self.spacewidth_)
    
    def getBitPos(self,id):
        for name,obj in self.objects.items():
            if "bit" in name:
                if self.getBitNumber_(name) == id:
                    x = obj.getPosX() + self.spacewidth_/2
                    y = obj.getPosY()
                    return [x,y]

    def setRandomInput(self):
        for name,obj in self.objects.items():
            if "bit" in name:
                obj.randomInput()
    def shadeActiveBits(self):
        for name,obj in self.objects.items():
            if "bit" in name:
                if obj.getBitValue() == 1:
                    obj.shadeBit(active=True,connected=True)

    def getBitNumber_(self,name):
        if "bit" in name:
            bitnum = name[ (name.find("bit")+3) : ]
            return int(bitnum)
        else:
            return -1

class Dendrite(Widget):
    def __init__(self,winsz,columns,inputspace,cell=-1,bit=1,perm=0.5):
        Widget.__init__(self,winsz,0,0)
        self.cols = columns
        self.inputs = inputspace
        self.cell = cell
        self.bit = bit
        self.perm = perm
        self.threshold = 0.3
        self.connected = False

        if self.perm > self.threshold:
            self.connected = True
        
        self.arrowPosA = [0,0]
        if cell == -1:
            self.arrowPosA = self.cols.getColPos(side="top")
        elif cell > 0:
            self.arrowPosA = self.cols.getCellPos(self.cell)
        self.arrowPosB = self.inputs.getBitPos(self.bit)

        self.objects["0.arrow1"] = Arrow(self.arrowPosA[0],self.arrowPosA[1],
                                        self.arrowPosB[0], self.arrowPosB[1],
                                        width=5,headsize=15)
        self.objects["1.permanenceBar"] = LoadingBar(winsz, self.arrowPosB[0]-10,self.arrowPosB[1]+50,100)
        self.objects["1.permanenceBar"].setProgress(100*self.perm)
        if self.connected == True:
            self.objects["1.permanenceBar"].setBarColor(r=50,g=255,b=50)
        else:
            self.objects["1.permanenceBar"].setBarColor(r=255,g=50,b=50)


class ColumnTestScene(Scene):
    def __init__(self,winsz):
        Scene.__init__(self,winsz)
        self.col1 = HTMColumn(winsz,100,100,3)
        self.input1 = InputSpace(winsz,100,400,10)
        self.dendrite = Dendrite(winsz,self.col1,self.input1,bit=8,perm=0.1)
        self.dendrite.objects["1.permanenceBar"].setVisible(False)

    def draw(self):
        self.col1.draw()
        self.input1.draw()
        self.dendrite.draw()
    
    def update(self,dt):
        self.deltat = self.deltat + dt
        if self.deltat == dt:
            self.input1.setRandomInput()
            self.input1.shadeActiveBits()
        if self.deltat > 3:
            self.dendrite.objects["1.permanenceBar"].setVisible(True)
