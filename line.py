# line.py
# Sam Gallagher
# 12 April 2018
#
# Line object for animations

class Line(object):
    def __init__(self, x1,y1, x2,y2, width=1, r=255,g=255,b=255,alpha=255):
        self.verts = (x1,y1, x2,y2)
        self.width = width
        self.rgba_ = (r, g, b, alpha)
