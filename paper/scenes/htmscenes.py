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
        
        self.center = -1

        self.width_ = 50
        self.height_ = 200
        self.ncells_ = 6
        self.cellrad_ = (self.width_*0.5)/2 #Cell takes up 50% of column width
        self.deltat = 0.0
        self.outlineWidth = 4
        self.objects["2.outline"] = Box(self.posx_-self.outlineWidth,self.posy_-self.outlineWidth, 
                                        self.width_ + 2*self.outlineWidth,self.height_ + 2*self.outlineWidth,
                                        r=0,g=0,b=0,alpha=255) #red outline box
        self.objects["3.background"] = Box(self.posx_,self.posy_, self.width_,self.height_) #White background box
        self.objects["0.overlapbox"] = Box(self.posx_,self.posy_-50,self.width_,50,r=150,g=150,b=150)
        self.objects["1.overlapscore"] = Text("0",self.posx_+15,self.posy_-25,rgba=[0,0,0,255])
        
        self.objects["0.overlapbox"].setVisible(False)
        self.objects["1.overlapscore"].setVisible(False)
        
        cellspacing = self.height_/(self.ncells_+1)
        for i in range(4,self.ncells_+4):
            self.objects[str(i)+".Cell" + str(i-3)] = Circle(self.posx_+self.width_/2,self.posy_+(i-3)*cellspacing,self.cellrad_,
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

    def showOverlap(self,show=True):
        if show:
            self.objects["0.overlapbox"].setVisible(True)
            self.objects["1.overlapscore"].setVisible(True)
        else:
            self.objects["0.overlapbox"].setVisible(False)
            self.objects["1.overlapscore"].setVisible(False)

    def setOverlap(self,overlap):
        self.objects["1.overlapscore"].setText(str(overlap))
    def setOutline(self,outline = True):
        if outline:
            self.objects["2.outline"].setColor(255,0,0,255)
        else:
            self.objects["2.outline"].setColor(0,0,0,255)
    def setActiveCells(self,activelist): 
        for name,obj in self.objects.items():  #Reset cell colors
            if "Cell" in name:
                obj.setColor(200,200,200)
                if self.getCellNumber_(name) in activelist:
                    obj.setColor(255,50,50)

    def fadeState(self,t,dt,tfade,startcolor,activecells = [],outline=False):
        if outline == True:
            self.objects["2.outline"].fadeState(t,dt,tfade,startcolor,[255,0,0,255])
        else:
            self.objects["2.outline"].fadeState(t,dt,tfade,startcolor,[0,0,0,255])

        ret = self.objects["3.background"].fadeState(t,dt,tfade,startcolor,[255,255,255,255])
        for name,obj in self.objects.items():
            if "Cell" in name:
                if self.getCellNumber_(name) in activecells:
                    obj.fadeState(t,dt,tfade,startcolor,[255,50,50,255])
                else:
                    obj.fadeState(t,dt,tfade,startcolor,[200,200,200,255])
        return ret
    
    def setCellPos_(self):
        cellspacing = self.height_/(self.ncells_+1)
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
    def shadeBit(self,active=True,connected=True,rgba=[]):
        if len(rgba) > 0:
            rgbaout = rgba
        elif active and connected:
            rgbaout = [155,250,155,255]
        elif active and not connected:
            rgbaout = [255,255,0,255]
        elif (not active) and connected:
            rgbaout = [255,155,155,255]
        elif (not active) and not connected:
            rgbaout = [255,255,255,255]
        self.objects["1.bg"].setColor(rgbaout[0],rgbaout[1],rgbaout[2],rgbaout[3])

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
    def getBitValue(self,id):
        for name,obj in self.objects.items():
            if self.getBitNumber_(name) == id:
                return obj.getBitValue()

    def setRandomInput(self):
        for name,obj in self.objects.items():
            if "bit" in name:
                obj.randomInput()
    def shadeBits(self,bits=[],active=True,connected=True,rgba=[]):
        for name,obj in self.objects.items():
            if "bit" in name:
                if self.getBitNumber_(name) in bits:
                    obj.shadeBit(active,connected,rgba)
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
    
    def getDendriteValue(self):
        return self.inputs.getBitValue(self.bit)
    def setPermanence(self,perm):
        if perm > 1:
            perm = 1
        elif perm < 0:
            perm = 0
        self.perm = perm
        if self.perm > self.threshold:
            self.connected = True
        
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
        self.overlap = 0
        self.objindex = 1
        if len(self.bits) != len(self.perms):
            print("Error: Bits and permanences must have the same size")
        elif len(self.bits) > self.inputs.getNumInputs():
            print("Error: Can't specify more bits than there are input bits")
        elif max(self.bits) > self.inputs.getNumInputs():
            print("Error: Can't specify a bit outside of the input space")
        else:
            for s in range(1,self.nsynapses+1):
                key = str(self.objindex) + ".dendrite" + str(s)
                self.objects[ key ] = Dendrite(self.sz_,self.cols,self.inputs,bit=self.bits[s-1],perm=self.perms[s-1],threshold=self.threshold)
                self.objindex = self.objindex + 1
    def showPermBars(self,show=True):
        for _,obj in self.objects.items():
            obj.setPermanenceBarVisible(show)
    def getDendriteValue(self,id):
        for name,obj in self.objects.items():
            if self.getDendriteNumber_(name) == id:
                return obj.getBitValue()
    def getOverlapScore(self):
        self.overlap = 0
        for name,obj in self.objects.items():
            if "dendrite" in name:
                if obj.connected and obj.getDendriteValue() == 1:
                    self.overlap = self.overlap + 1
        return self.overlap

    def shadeConnectedDendrites(self,shade=True):
        if shade == True:
            bits = []
            for name,obj in self.objects.items():
                if "dendrite" in name:
                    if obj.connected == True:
                        bits.append(obj.bit)
            self.inputs.shadeBits(bits,connected=True)
        else:
            self.inputs.unshadeAllBits()
    def shadeUnconnectedDendrites(self,shade=True):
        if shade == True:
            bits = []
            for name,obj in self.objects.items():
                if "dendrite" in name:
                    if obj.connected == False:
                        bits.append(obj.bit)
            self.inputs.shadeBits(bits,rgba=[150,150,150,255])
        else:
            self.inputs.unshadeAllBits()
    def shadeDendrites(self,shade=True):
        # Shades dendrites based on activity and connectedness
        if shade == True:
            for name,obj in self.objects.items():
                if "dendrite" in name:
                    if obj.connected==True and obj.getDendriteValue()==1:
                        self.inputs.shadeBits([obj.bit],active=True,connected=True)
                    elif obj.connected==True and obj.getDendriteValue()==0:
                        self.inputs.shadeBits([obj.bit],active=False,connected=True)
                    elif obj.connected==False and obj.getDendriteValue()==1:
                        self.inputs.shadeBits([obj.bit],active=True,connected=False)
                    elif obj.connected==False and obj.getDendriteValue()==0:
                        self.inputs.shadeBits([obj.bit],active=False,connected=False)
        else:
            self.inputs.unshadeAllBits()

    def setDendrites(self,bits=[],perms=[],threshold=0.2):
        if len(bits) == len(perms):
            self.bits = bits
            self.perms = perms
            self.threshold = threshold
            self.nsynapses = len(self.bits)
            self.objindex = 1
            self.obejcts = {}
            for s in range(1,self.nsynapses+1):
                key = str(self.objindex) + ".dendrite" + str(s)
                self.objects[ key ] = Dendrite(self.sz_,self.cols,self.inputs,bit=self.bits[s-1],perm=self.perms[s-1],threshold=self.threshold)
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
        for c in range(1,nsynapses+1):
            rpos = random.randint(lowlimit,highlimit)
            while rpos in bits:
                rpos = random.randint(lowlimit,highlimit)
            bits.append(rpos)
            perms.append(0.0)
        self.setDendrites(bits,perms)
        self.updateSynapses_()
    def setRandomPerms(self,dist = "normal"):
        np.random.seed(int(math.floor(clock()*1e5)))
        bits = self.bits
        perms = []
        for c in range(1,self.nsynapses+1):
            if dist == "normal":
                perms.append(abs(np.random.normal(self.threshold,0.08)))
        self.setDendrites(bits,perms)
        self.updateSynapses_()
    def setRandomDendrites(self,nsynapses,lowlimit=1,highlimit=-1):
        self.setRandomLocations(nsynapses,lowlimit=lowlimit,highlimit=highlimit)
        self.setRandomPerms()
        self.updateSynapses_()
        # Sets random positions and permanences 
    def calculateSynapses(self, inc, dec):
        for name,obj in self.objects.items():
            if "dendrite" in name:
                if obj.getDendriteValue() == 1:
                    obj.setPermanence(obj.perm + inc)
                else:
                    obj.setPermanence(obj.perm - dec)
        self.updateSynapses_()

    def updateSynapses_(self):
        for name,obj in self.objects.items():
            if "dendrite" in name:
                if obj.perm > obj.threshold:
                    obj.connected = True
    def getDendriteNumber_(self,name):
        if "dendrite" in name:
            dendnum = name[ (name.find("dendrite")+8) : ]
            return int(dendnum)
        else:
            return -1


class SpatialParameters(object):
    def __init__(self,inputwidth,colpct,inhibitionradius,minoverlap,threshold,globalreceptivefield,receptivefieldsize,syninc,syndec):
        """
        Spatial pooling parameters for use initializing a column space.

        @params
        inputwidth              Number of spaces in the input space
        colpct                  Sets size of column space by colpct percent of the inputwidth
        colactivepct            Percent of columns in an inhibition radius that are active
        inhibitionradius        Number of columns compared for activity
        minoverlap              Minimum column overlap for consideration of activity
        threshold               Synapse connection threshold
        globalreceptivefield    Boolean for global receptive fields
        receptivefieldsize      Receptive field size per column. Only needed if globalreceptivefield is False
        syninc                  Synapse permanence increment
        syndec                  Synapse permanence decrement
        """
        self.inputwidth = inputwidth
        self.colpct = colpct
        self.inhibitionradius = inhibitionradius
        self.minoverlap = minoverlap
        self.threshold = threshold
        self.globalreceptivefield = globalreceptivefield
        self.receptivefieldsize = receptivefieldsize
        self.syninc = syninc
        self.syndec = syndec

class ColumnSpace(Widget):
    def __init__(self,winsz,inputspace,spatialparams,height,width):
        """
        A column space, which implements the Spatial Pooling algorithm. 
        
        @params
        inputspace      The InputSpace for the columns
        height          The y-position of the column space
        """
        Widget.__init__(self,winsz,0,0)
        self.input = inputspace
        self.params = spatialparams
        self.ncols = math.floor(self.params.inputwidth*self.params.colpct)
        self.overlaps = []

        # Distribute the columns through the width of the screen
        colspacing = width/(self.ncols + 1)/2
        posx = self.sz_[0]/2 - width/2
        coln = 1

        for c in range(1,(self.ncols)*2+1,2):
            # Make a column and dendrite pair
            keyc = str(c) + ".column" + str(coln)
            keyd = str(c+1) + ".dendrite" + str(coln)
            self.objects[keyc] = HTMColumn(winsz,posx + colspacing*c,100,3)
            self.objects[keyd] = ProximalDendriteSegment(winsz, self.objects[keyc],self.input,[1],[0.0],threshold=self.params.threshold)
            
            # Initialize dendrites
            if self.params.globalreceptivefield:
                self.objects[keyd].setRandomDendrites(math.ceil(self.params.inputwidth*0.8))
            else:
                colcenter = math.floor(self.params.inputwidth/(self.ncols))*coln
                left = colcenter - math.ceil(self.params.receptivefieldsize/2)
                right = colcenter + math.floor(self.params.receptivefieldsize/2)
                if left < 1:
                    left = 1
                if right > self.params.inputwidth:
                    right = self.params.inputwidth
                self.objects[keyc].center = colcenter
                self.objects[keyd].setRandomDendrites(math.ceil(self.params.receptivefieldsize*1.0)-1,left,right)
            
            self.objects[keyd].setVisible(False)
            coln = coln + 1
    def updateColOverlaps(self):
        self.overlaps = [0 for x in range(self.ncols)]
        for name,obj in self.objects.items():
            if "column" in name:
                colnumber = self.getColNumber_(name)
                dendrite = self.getColDendrite_(colnumber)
                obj.setOverlap(dendrite.getOverlapScore())
                self.overlaps[colnumber-1] = dendrite.getOverlapScore()
    def updateColSynapses(self):
        for name,obj in self.objects.items():
            if "dendrite" in name:
                obj.calculateSynapses(self.params.syninc,self.params.syndec)

    def showColOverlap(self,col=-1,show=True):
        if show:
            if col > 0:
                for name,obj in self.objects.items():
                    if self.getColNumber_(name) == col:
                        obj.showOverlap()
            else:
                for name,obj in self.objects.items():
                    if "column" in name:
                        obj.showOverlap()
        else:
            for name,obj in self.objects.items():
                if "column" in name:
                    obj.showOverlap(False)

    def showColDendrite(self,col=-1,show=True):
        if show == True:
            if col == -1:
                for name,obj in self.objects.items():
                    if "dendrite" in name:
                        obj.setVisible(True)
            elif col > 0:
                for name,obj in self.objects.items():
                    if self.getDendriteSegmentNumber_(name) == col:
                        obj.setVisible(True)
        else:
            for name,obj in self.objects.items():
                if "dendrite" in name:
                    obj.setVisible(False)
    def shadeColCenter(self,col=-1,shade=True,rgba=[]):
        """ Shades or unshades column center. If col == -1, all column centers are highlighted."""
        if len(rgba) == 0:
            rgba = [255,150,150,255]
        if shade == True:
            if col == -1:
                for name,obj in self.objects.items():
                    if "column" in name:
                        self.input.shadeBits([obj.center],rgba=rgba)
            elif col > 0:
                for name,obj in self.objects.items():
                    if "column" in name:
                        if self.getColNumber_(name) == col:
                            self.input.shadeBits([obj.center],rgba=rgba)
        else:
            self.input.unshadeAllBits()
    def shadeColReceptiveField(self,col=-1,shade=True):
        if shade == True:
            if col > 0:
                for name,obj in self.objects.items():
                    if "column" in name:
                        self.input.shadeBits(self.getColReceptiveField(col),rgba=[255,150,150,255])
                self.shadeColCenter(col=col,rgba=[255,50,50,255])
        else:
            self.input.unshadeAllBits()
    def findActiveCols(self):
        activecols = [1,2] # top 2 columns
        for c in range(2,len(self.overlaps)+1):
            if self.overlaps[c-1] > self.overlaps[activecols[0]-1]:
                activecols[1] = activecols[0]
                activecols[0] = c
            elif self.overlaps[c-1] > self.overlaps[activecols[1]-1]:
                activecols[1] = c
        for name,obj in self.objects.items():
            if "column" in name:
                if self.getColNumber_(name) in activecols:
                    obj.setOutline(True)
                else:
                    obj.setOutline(False)

    def getColReceptiveField(self,col=1):
        colcenter = -1
        for name,obj in self.objects.items():
            if self.getColNumber_(name) == col:
                colcenter = obj.center
        left = colcenter - math.ceil(self.params.receptivefieldsize/2)
        right = colcenter + math.ceil(self.params.receptivefieldsize/2)
        if left < 1:
            left = 1
        if right > self.params.inputwidth:
            right = self.params.inputwidth
        bits = []
        for b in range(left,right+1):
            bits.append(b)
        return bits
    def shadeColConnectedDendrites(self,col=1,shade=True):
        if shade == True:
            self.getColDendrite_(col).shadeConnectedDendrites()
            self.getColDendrite_(col).shadeUnconnectedDendrites()
        else:
            self.getColDendrite_(col).shadeConnectedDendrites(shade=False)
            self.getColDendrite_(col).shadeUnconnectedDendrites(shade=False)
    def shadeColDendrites(self,col=1,shade=True):
        if shade == True:
            self.getColDendrite_(col).shadeDendrites()
        else:
            self.getColDendrite_(col).shadeDendrites(shade=False)

    def getColNumber_(self,name):
        if "column" in name:
            colnum = name[ (name.find("column")+6) : ]
            return int(colnum)
        else:
            return -1
    def getDendriteSegmentNumber_(self,name):
        if "dendrite" in name:
            dendnum = name[ (name.find("dendrite")+8) : ]
            return int(dendnum)
        else:
            return -1
    def getColDendrite_(self,col=1):
        for name,obj in self.objects.items():
            if "dendrite" in name:
                if self.getDendriteSegmentNumber_(name) == col:
                    return obj


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
        self.input = InputSpace(winsz,100,400,32)
        self.spParams = SpatialParameters(inputwidth=32, colpct=0.20, inhibitionradius=4, minoverlap=0, threshold=0.2,
                                        globalreceptivefield=False, receptivefieldsize=8, syninc=0.5, syndec=0.5)
        self.colspace = ColumnSpace(winsz,self.input,self.spParams,200,500)

        # Text
        self.title = Text("HTM Spatial Pooling",winsz[0]/2,winsz[1]-30,anchorx='center')
        self.description = Text("Let's bring in more columns. We will initialize each column with a center and potential dendrites covering 80% of the receptive field.",
                                winsz[0]/2-100, 40, fontsize=15,multiline=True,width=winsz[0]/2+50)


    def draw(self):
        self.input.draw()
        self.colspace.draw()
        self.title.draw()
        self.description.draw()
    
    def update(self,dt,keypress=False):
        self.deltat = self.deltat + dt

        if self.state_ == "init":
            if keypress:
                self.state_ = "showcol1dendrite"
        
        ### SHOW COLUMN DENDRITES ###
        elif self.state_ == "showcol1dendrite":
            self.colspace.showColDendrite(col=1)
            self.description.setText("This is the dendrite for column 1, on the far left.")
            if keypress:
                self.state_ = "showcol1center"
        elif self.state_ == "showcol1center":
            self.colspace.shadeColCenter(col=1)
            self.description.setText("The center for column 1 is highlighted in red.")
            if keypress:
                self.state_ = "showcol1rfield"
        elif self.state_ == "showcol1rfield":
            self.colspace.shadeColReceptiveField(col=1)
            self.description.setText("This is the receptive field of column 1. This is the range of the input space it could use for potential connections.")
            if keypress:
                self.state_ = "showcol2"
        elif self.state_ == "showcol2":
            self.colspace.shadeColReceptiveField(shade=False)
            self.colspace.showColDendrite(col=1,show=False)
            self.colspace.showColDendrite(col=2)
            self.colspace.shadeColReceptiveField(col=2)
            self.description.setText("The other columns are initialized in the same way.")
            if keypress:
                self.state_ = "showcol3"
        elif self.state_ == "showcol3":
            self.colspace.shadeColReceptiveField(shade=False)
            self.colspace.showColDendrite(col=2,show=False)
            self.colspace.showColDendrite(col=3)
            self.colspace.shadeColReceptiveField(col=3)
            if keypress:
                self.state_ = "showcol4"
        elif self.state_ == "showcol4":
            self.colspace.shadeColReceptiveField(shade=False)
            self.colspace.showColDendrite(col=3,show=False)
            self.colspace.showColDendrite(col=4)
            self.colspace.shadeColReceptiveField(col=4)
            if keypress:
                self.state_ = "showcol5"
        elif self.state_ == "showcol5":
            self.colspace.shadeColReceptiveField(shade=False)
            self.colspace.showColDendrite(col=4,show=False)
            self.colspace.showColDendrite(col=5)
            self.colspace.shadeColReceptiveField(col=5)
            if keypress:
                self.state_ = "showcol6"
        elif self.state_ == "showcol6":
            self.colspace.shadeColReceptiveField(shade=False)
            self.colspace.showColDendrite(col=5,show=False)
            self.colspace.showColDendrite(col=6)
            self.colspace.shadeColReceptiveField(col=6)
            if keypress:
                self.state_ = "col6text1"
        elif self.state_ == "col6text1":
            self.description.setText("Notice how column 6's receptive field is cut off. We could instead have it 'roll over' and use cells on the left of the input space.")
            if keypress:
                self.state_ = "col6text2"
        elif self.state_ == "col6text2":
            self.description.setText("This is called wrap around, and it can give columns at the edges a better chance at being active. ")
            if keypress:
                self.state_ = "hidedendrites"
        elif self.state_ == "hidedendrites":
            self.colspace.shadeColReceptiveField(shade=False)
            self.colspace.showColDendrite(col=6,show=False)
            self.description.setText("Each column has a few connected synapses out of its potential connections. Let's look at column 1 again.")
            if keypress:
                self.state_ = "showcol1again"
        

        ### COLUMN 1 IN DETAIL ###
        elif self.state_ == "showcol1again":
            self.colspace.showColDendrite(col=1,show=True)
            self.description.setText("Column 1 can only see its receptive field, from which it will have the chance to connect to some of the spaces (the arrows).")
            if keypress:
                self.state_ = "col1text2"
        elif self.state_ == "col1text2":
            self.colspace.shadeColConnectedDendrites(col=1,shade=True)
            self.description.setText("From its potential connections, only the dendrites with permanences over the threshold are actually used by the column.")
            if keypress:
                self.state_ = "col1text3"
        elif self.state_ == "col1text3":
            self.description.setText("We can see bits based on whether they are active (1) or inactive (0), and whether the dendrite synapse is connected or not.")
            self.colspace.shadeColConnectedDendrites(col=1,shade=False)
            self.colspace.shadeColDendrites(col=1,shade=True)
            self.state_ = "col1text4"
        elif self.state_ == "col1text4":
            self.description.setText("We have four states. Connected dendrite to active bit, connected dendrite to inactive bit, unconnected dendrite to active"+
                                    " bit, and unconnected dendrite to inactive bit.")
            if keypress:
                self.state_ = "randomdatatext"
        elif self.state_ == "randomdatatext":
            self.description.setText("This is not too interesting without data, so let's bring in some random bits.")
            if keypress:
                self.state_ = "randomdata"
        elif self.state_ == "randomdata":
            self.input.setRandomInput()
            self.colspace.shadeColDendrites(col=1,shade=True)
            self.state_ = "legendtext"
        elif self.state_ == "legendtext":
            self.description.setText("Here, green spaces are active and connected, yellow are active but not connected, and red are inactive but connected.")
            if keypress:
                self.state_ = "overlapscore"
        
        ### OVERLAP SCORE ###
        elif self.state_ == "overlapscore":
            self.description.setText("For a column, the number of synapses that are connected to active bits is called the 'overlap' of the column.")
            if keypress:
                self.state_ = "overlaptext2"
        elif self.state_ == "overlaptext2":
            self.description.setText("The overlap, or overlap score, of each column is used to determine which columns can be active. ")
            if keypress:
                self.state_ = "overlaptext3"
        elif self.state_ == "overlaptext3":
            self.description.setText("We compare a few columns at a time, and the top N columns with the highest overlap scores of those are chosen to be active at this time.")
            if keypress:
                self.state_ = "showoverlapscore"
        elif self.state_ == "showoverlapscore":
            self.description.setText("Here is the overlap score for column 1.")
            self.colspace.updateColOverlaps()
            self.colspace.showColOverlap(1)
            self.state_ = "wait"
        elif self.state_ == "wait":
            if keypress:
                self.state_ = "alloverlaptext"
        elif self.state_ == "alloverlaptext":
            self.description.setText("We can repeat this process for all the other columns.")
            self.colspace.shadeColDendrites(shade=False)
            self.colspace.showColDendrite(show=False)
            if keypress:
                self.state_ = "showalloverlaps"
        elif self.state_ == "showalloverlaps":
            self.colspace.showColDendrite()
            self.colspace.showColOverlap()
            if keypress:
                self.state_ = "getactives"
        elif self.state_ == "getactives":
            self.colspace.findActiveCols()
            self.description.setText("We'll select the top 2 columns as the active columns, from all columns. This is called global inhibition.")
            if keypress:
                self.state_ = "neighborhoods"
        elif self.state_ == "neighborhoods":
            self.description.setText("The other option is to break the column space up into 'neighborhoods' where the top columns from each neighborhood are chosen.")
            if keypress:
                self.state_ = "spatialpooling"
        elif self.state_ == "spatialpooling":
            self.description.setText("The active columns at this time step will characterize the input, and by the nature of overlaps, similar inputs will return similar outputs.")
            if keypress:
                self.state_ = "sptext2"
        elif self.state_ == "sptext2":
            self.colspace.showColDendrite(show=False)
            self.colspace.showColOverlap(show=False)
            self.description.setText("Now that we have seen the active columns at this time step, we will update synapses in all the columns.")
            if keypress:
                self.state_ = "updatesyn1"
        elif self.state_ == "updatesyn1":
            self.description.setText("All synapses, connected or disconnected, are updated each time step during learning.")
            if keypress:
                self.state_ = "updatesyn2"
        elif self.state_ == "updatesyn2":
            self.description.setText("If the synapse was connected to a 1, an active bit, its permanence is incremented. If the bit was a 0, an inactive bit, the permanence is decremented.")
            if keypress:
                self.state_ = "col1syn"
        elif self.state_ == "col1syn":
            self.description.setText("Let's look at column 1 again.")
            self.colspace.showColDendrite(col=1)
            if keypress:
                self.state_ = "col1syn2"
        elif self.state_ == "col1syn2":
            self.description.setText("We update synapse permanences, and then check which synapses are now connected or disconnected. Let's see an extreme example.")
            if keypress:
                self.state_ = "col1synupdate"
        elif self.state_ == "col1synupdate":
            self.colspace.updateColSynapses()
            self.description.setText("Each time step typically results in a small change in synapse permanence, but here we've used large increments and decrements.")
            if keypress:
                self.state_ = "end"
        elif self.state_ == "end":
            self.colspace.showColDendrite(show=False)
            self.description.setText("After all synapses are updated, spatial pooling at this time step is complete, the column activity is returned, and we're ready for the next input.")


            