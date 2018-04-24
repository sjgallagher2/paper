# Animation object for an HTM column
import math
import pyglet
import random
import os
import numpy as np
from time import clock
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
        self.outlineWidth = 4
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

    def fadeState(self,t,dt,tfade,startcolor,activecells = [],outline=False):
        if outline == True:
            self.objects["0.outline"].fadeState(t,dt,tfade,startcolor,[255,0,0,255])
        else:
            self.objects["0.outline"].fadeState(t,dt,tfade,startcolor,[0,0,0,255])

        ret = self.objects["1.background"].fadeState(t,dt,tfade,startcolor,[255,255,255,255])
        for name,obj in self.objects.items():
            if "Cell" in name:
                if self.getCellNumber_(name) in activecells:
                    obj.fadeState(t,dt,tfade,startcolor,[255,50,50,255])
                else:
                    obj.fadeState(t,dt,tfade,startcolor,[200,200,200,255])
        return ret
    
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
        if active and connected:
            rgba = [155,250,155,255]
        elif active and not connected:
            rgba = [255,255,0,255]
        elif (not active) and connected:
            rgba = [255,155,155,255]
        elif (not active) and not connected:
            rgba = [255,255,255,255]
        self.objects["1.bg"].setColor(rgba[0],rgba[1],rgba[2],rgba[3])

    def unshadeBit(self):
        self.objects["1.bg"].setColor(r=255,g=255,b=255,alpha=255)
    
    def fadeShadeState(self,t,dt,tfade,active=True,connected=True):
        #Get color
        if active and connected:
            rgba = [155,250,155,255]
        elif active and not connected:
            rgba = [255,255,0,255]
        elif (not active) and connected:
            rgba = [255,155,155,255]
        elif (not active) and not connected:
            rgba = [255,255,255,255]
        #Go to fade function
        return self.objects["1.bg"].fadeState(t,dt,tfade,[255,255,255,255],rgba)
    def fadeUnshadeState(self,t,dt,tfade):
        rgba = self.objects["1.bg"].getColor()
        return self.objects["1.bg"].fadeState(t,dt,tfade,rgba,[255,255,255,255])

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
    def getNumInputs(self):
        return self.nspaces_

    def setRandomInput(self):
        for name,obj in self.objects.items():
            if "bit" in name:
                obj.randomInput()
    def shadeActiveBits(self):
        for name,obj in self.objects.items():
            if "bit" in name:
                if obj.getBitValue() == 1:
                    obj.shadeBit(active=True,connected=True)
    def unshadeAllBits(self):
        for name,obj in self.objects.items():
            if "bit" in name:
                obj.unshadeBit()
    def fadeShadeActiveState(self,t,dt,tfade=1):
        for name,obj in self.objects.items():
            if "bit" in name:
                if obj.getBitValue() == 1:
                    ret = obj.fadeShadeState(t,dt,tfade,active=True,connected=True)
        return ret
    def fadeUnshadeState(self,t,dt,tfade=1):
        for name,obj in self.objects.items():
            if "bit" in name:
                ret = obj.fadeUnshadeState(t,dt,tfade)
        return ret

    def getBitNumber_(self,name):
        if "bit" in name:
            bitnum = name[ (name.find("bit")+3) : ]
            return int(bitnum)
        else:
            return -1

class Dendrite(Widget):
    def __init__(self,winsz,columns,inputspace,cell=-1,bit=1,perm=0.5,threshold=0.3):
        Widget.__init__(self,winsz,0,0)
        self.cols = columns
        self.inputs = inputspace
        self.cell = cell
        self.bit = bit
        self.perm = perm
        self.threshold = threshold
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
                                        width=3,headsize=20,headang=15)
        self.objects["1.permanenceBar"] = LoadingBar(winsz, self.arrowPosB[0]-10,self.arrowPosB[1]+50,height=70)
        self.objects["1.permanenceBar"].setProgress(100*self.perm)
        if self.connected == True:
            self.objects["1.permanenceBar"].setBarColor(r=50,g=255,b=50)
        else:
            self.objects["1.permanenceBar"].setBarColor(r=255,g=50,b=50)
    
    def setPermanenceBarVisible(self,visible = True):
        self.objects["1.permanenceBar"].setVisible(visible)

class ProximalDendriteSegment(Widget):
    def __init__(self,winsz,columns,inputs,bits=[],perms=[],threshold=0.2):
        Widget.__init__(self,winsz,0,0)
        self.cols = columns
        self.inputs = inputs
        self.bits = bits
        self.perms = perms
        self.threshold = threshold
        self.nsynapses = len(self.bits)
        self.objindex = 1
        if len(self.bits) != len(self.perms):
            print("Error: Bits and permanences must have the same size")
        elif len(self.bits) > self.inputs.getNumInputs():
            print("Error: Can't specify more bits than there are input bits")
        elif max(self.bits) > self.inputs.getNumInputs():
            print("Error: Can't specify a bit outside of the input space")
        else:
            for s in range(0,self.nsynapses):
                key = str(self.objindex) + ".synapse" + str(s)
                self.objects[ key ] = Dendrite(self.sz_,self.cols,self.inputs,bit=self.bits[s],perm=self.perms[s],threshold=self.threshold)
                self.objindex = self.objindex + 1
    def showPermBars(self,show=True):
        for _,obj in self.objects.items():
            obj.setPermanenceBarVisible(show)
    def setDendrites(self,bits=[],perms=[],threshold=0.2):
        if len(bits) == len(perms):
            self.bits = bits
            self.perms = perms
            self.threshold = threshold
            self.nsynapses = len(self.bits)
            self.objindex = 1
            self.obejcts = {}
            for s in range(0,self.nsynapses):
                key = str(self.objindex) + ".synapse" + str(s)
                self.objects[ key ] = Dendrite(self.sz_,self.cols,self.inputs,bit=self.bits[s],perm=self.perms[s],threshold=self.threshold)
                self.objindex = self.objindex + 1
        else:
            print("Error: Number of bits and permanences must be equal")
    def setRandomLocations(self,nsynapses,lowlimit=1,highlimit=-1):
        """Sets nsynapses random connections to the input space between lowlimit and highlimit"""
        random.seed()
        self.nsynapses = nsynapses
        if highlimit < lowlimit or highlimit > self.inputs.getNumInputs():
            highlimit = self.inputs.getNumInputs()
        bits = []
        perms = []
        for c in range(0,nsynapses):
            bits.append(random.randint(lowlimit,highlimit))
            perms.append(0.0)
        self.setDendrites(bits,perms)
    def setRandomPerms(self,dist = "normal"):
        np.random.seed(int(math.floor(clock()*1e5)))
        bits = self.bits
        perms = []
        for c in range(0,self.nsynapses):
            if dist == "normal":
                perms.append(abs(np.random.normal(self.threshold,0.08)))
        self.setDendrites(bits,perms)
        
    def setRandomDendrites(self,nsynapses):
        self.setRandomLocations(nsynapses)
        self.setRandomPerms()
        # Sets random positions and permanences 

class ColumnScene(Scene):
    def __init__(self,winsz):
        Scene.__init__(self,winsz)
        self.col1 = HTMColumn(winsz,100,100,3)
        self.input1 = InputSpace(winsz,100,400,32)
        self.dendrites = ProximalDendriteSegment(winsz,self.col1,self.input1,bits=[1,2,4,8],perms=[0.0,0.0,0.0,0.0],threshold=0.2)
        self.receptivefieldsize = 15
        self.receptivefield1 = Arrow(100,390,105,390,width=8,headsize=24,r=255,g=0,b=0)
        self.receptivefield2 = Arrow(150,390,155,290,width=8,headsize=24,r=255,g=0,b=0)
        
        self.input1.setVisible(False)
        self.col1.setVisible(False)
        self.dendrites.setVisible(False)
        self.receptivefield1.setVisible(False)
        self.receptivefield2.setVisible(False)

        # Text
        self.title = Text("HTM Spatial Pooling",winsz[0]/2,winsz[1]-30,anchorx='center',rgba=[0,0,0,255])
        self.description = Text("Assume we have some binary data",
                                winsz[0]/2-100, 70, fontsize=15,multiline=True,width=winsz[0]/2+50,rgba=[0,0,0,255])


    def draw(self):
        self.col1.draw()
        self.input1.draw()
        self.dendrites.draw()
        self.receptivefield1.draw()
        self.receptivefield2.draw()
        self.title.draw()
        self.description.draw()
    
    def update(self,dt,keypress=False):
        self.deltat = self.deltat + dt
        if self.state_ == "init":
            if keypress:
                self.deltat = 0.0
                self.state_ = "fadeintitle"

        ### FADE IN ###
        elif self.state_ == "fadeintitle":
            if self.title.fadeState(self.deltat,dt,0.5,[0,0,0,255],[255,255,255,255]) == -1:
                self.deltat = 0
                self.state_ = "fadeintext"
        elif self.state_ == "fadeintext":
            if self.description.fadeState(self.deltat,dt,0.5,[0,0,0,255],[255,255,255,255]) == -1:
                self.state_ = "wait1"
        elif self.state_ == "wait1":
            if keypress:
                self.state_ = "showinput"
        elif self.state_ == "showinput":
            self.input1.setVisible(True)
            self.state_ = "wait2"
        elif self.state_ == "wait2":
            if keypress:
                self.state_ = "makerandinput"


        ### MAKE DATA ###
        elif self.state_ == "makerandinput":
            self.description.setText("And let's make the data random")
            self.input1.setRandomInput()
            self.input1.shadeActiveBits()
            self.state_ = "wait3"
            self.deltat = 0
        elif self.state_ == "wait3":
            if self.deltat > 1:
                self.deltat = 0.0
                self.state_ = "unshadeinput"
        elif self.state_ == "unshadeinput":
            if self.input1.fadeUnshadeState(self.deltat,dt) == -1:
                if keypress:
                    self.deltat = 0.0
                    self.state_ = "newcolumntext"

        ### MAKE COLUMN ###
        elif self.state_ == "newcolumntext":
            self.description.setText("To compress the input, HTM uses 'columns' which can be active (1) or inactive (0) depending on the input space.")
            if keypress:
                self.deltat = 0.0
                self.state_ = "showcolumn"
        elif self.state_ == "showcolumn":
            if self.deltat == dt:
                self.col1.setVisible(True)
            if self.col1.fadeState(self.deltat,dt,1,[0,0,0,255]) == -1:
                if keypress:
                    self.state_ = "colactiveexample"
        elif self.state_ == "colactiveexample":
            self.col1.setOutline()
            self.description.setText("Here the column is active, and can be considered a '1' in the column space.")
            if keypress:
                self.state_ = "colinactiveexample"
        elif self.state_ == "colinactiveexample":
            self.col1.setOutline(False)
            self.description.setText("Now the column in inactive, and can be considered a '0' in the column space.")
            if keypress:
                self.state_ = "dendritetext"

        ### MAKING DENDRITES ###
        elif self.state_ == "dendritetext":
            self.description.setText("Each column can 'connect' to spaces in the input space, and each connection is called a dendrite. A dendrite has a synapse," + 
                                    " which represents the strength of the connection, with a permanence between 0 and 1.")
            if keypress:
                self.state_ = "dendritetext2"
        elif self.state_ == "dendritetext2":
            self.description.setText("A column can only connect to some elements of the input space, and of those potential connections, only the ones with the" + 
                                    " strongest permanences are used by the column.")
            if keypress:
                self.state_ = "showdendrite"
        elif self.state_ == "showdendrite":
            self.dendrites.setRandomLocations(6,highlimit=15)
            #self.dendrites.setRandomPerms()
            self.dendrites.setVisible(True)
            self.dendrites.showPermBars(False)
            self.description.setText("These arrows represent potential connections, each pointing to a location in the input space.")
            self.state_ = "wait4"
        elif self.state_ == "wait4":
            if keypress:
                self.state_ = "showperms"
        elif self.state_ == "showperms":
            self.dendrites.showPermBars()
            self.description.setText("We can represent permanences with loading bars. If the permanence is above a certain level, the synapse is 'connected'.")
            if keypress:
                self.state_ = "randdendtext"
        elif self.state_ == "randdendtext":
            self.description.setText("Initially, dendrites are made at random within a range in the input space. The permanences are set randomly around the threshold.")
            if keypress:
                self.state_ = "randomperms"
        elif self.state_ == "randomperms":
            self.dendrites.setRandomPerms()
            self.state_ = "permstext2"
        elif self.state_ == "permstext2":
            self.description.setText("Here, the connection threshold is at 0.2 (20%). Green bars indicate a connected synapse.")
            if keypress:
                self.state_ = "receptivefieldtext"
        elif self.state_ == "receptivefieldtext":
            self.description.setText("The portion of the input space a column can reach is called the 'receptive field' of the column. This is the range of" + 
                                    " the input space the column can use to select potential connections.")
            if keypress:
                self.state_ = "setrecepfield"
        elif self.state_ == "setrecepfield":
            center = math.ceil(self.receptivefieldsize/2)
            centerpos = self.input1.getBitPos(center)
            self.receptivefield1.setPosA(centerpos[0],centerpos[1])
            self.receptivefield1.setPosB(centerpos[0] - 5, centerpos[1])
            self.receptivefield2.setPosA(centerpos[0],centerpos[1])
            self.receptivefield2.setPosB(centerpos[0] + 5,centerpos[1])
            self.deltat = 0
            self.state_ = "extendreceptarrows"
        elif self.state_ == "extendreceptarrows":
            self.receptivefield1.setVisible(True)
            self.receptivefield2.setVisible(True)
            leftstop = self.input1.getBitPos(1)
            rightstop = self.input1.getBitPos(self.receptivefieldsize)
            self.receptivefield1.extendState(self.deltat,dt,0.8,leftstop[0]-20,leftstop[1])
            if self.receptivefield2.extendState(self.deltat,dt,0.8,rightstop[0]+20,rightstop[1]) == -1:
                self.state_ = "receptivefieldtext2"
        elif self.state_ == "receptivefieldtext2":
            self.description.setText("The middle of the receptive field is called the column center. A column can also have a global receptive field, meaning " + 
                                    "it can select its potential connections from the total input space.")
            if keypress:
                self.state_ = "recepfieldtext3"
        elif self.state_ == "recepfieldtext3":
            self.receptivefield1.setVisible(False)
            self.receptivefield2.setVisible(False)
            self.description.setText("Remember that the column's potential connections are chosen from the receptive field, and only the connected synapses are used" + 
                                    " to determine whether the column is active or not.")
            if keypress:
                self.state_ = "end"

        ### END STATE ###
        elif self.state_ == "end":
            pass
            #pyglet.app.exit()
        

class SpatialPoolerScene(Scene):
    def __init__(self,winsz):
        Scene.__init__(self,winsz)
        self.col1 = HTMColumn(winsz,100,100,3)
        self.col2 = HTMColumn(winsz,200,100,3)
        self.col3 = HTMColumn(winsz,300,100,3)
        self.col4 = HTMColumn(winsz,400,100,3)
        self.col5 = HTMColumn(winsz,500,100,3)
        self.input1 = InputSpace(winsz,100,400,30)
        self.dendrites1 = ProximalDendriteSegment(winsz,self.col1,self.input1,bits=[1,2,4,8],perms=[0.1,0.2,0.3,0.5],threshold=0.2)
        self.dendrites1.setVisible(False)

        # Text
        self.title = Text("HTM Spatial Pooling",winsz[0]/2,winsz[1]-30,anchorx='center')
        self.description = Text("Columns are objects that are active (1) or inactive (0) depending on the input space.",
                                winsz[0]/2-100, 70, fontsize=15,multiline=True,width=winsz[0]/2+50)


    def draw(self):
        self.col1.draw()
        self.col2.draw()
        self.col3.draw()
        self.col4.draw()
        self.col5.draw()
        self.input1.draw()
        self.dendrites1.draw()
        self.title.draw()
        self.description.draw()
    
    def update(self,dt,keypress=False):
        self.deltat = self.deltat + dt

