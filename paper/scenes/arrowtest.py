
from paper.core import Scene
from paper.primitives import Arrow

class TestArrowScene(Scene):
    def __init__(self,winsz):
        Scene.__init__(self,winsz)
        self.arrow1 = Arrow(200,200,230,230,width=3,headsize=10)
        self.deltat = 0.0

    def draw(self):
        self.arrow1.draw()

    def update(self, dt):
        if self.state_ == "init":
            self.arrow1.setColor(0,0,0,255)
            self.arrow1.setDirection(5000,100,absolute=True)
            self.state_ = "wait"

        elif self.state_ == "wait":
            if self.deltat > 1.5:
                self.deltat = 0
                self.state_ = "show"
            else:
                self.deltat = self.deltat + dt

        elif self.state_ == "show":
            self.arrow1.setColor(255,255,255,255)
            self.state_ = "draw"
        
        elif self.state_ == "draw":
            if self.arrow1.getLength() < 200:
                self.arrow1.scaleLength(1.1)
            else:
                self.state_ = "default"
        
        elif self.state_ == "default":
            pass
