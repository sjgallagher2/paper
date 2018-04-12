# circle.py
# Sam Gallagher
# 12 April 2018
#
# Circle object for animations

class Circle(object):
    def __init__(self, posx,posy,rad,r=255,g=255,b=255,alpha=255):
        self.posx = posx
        self.posy = posy
        self.rad = rad
        self.rgba_ = (r, g, b, alpha)