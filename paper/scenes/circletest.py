
from paper.core import Scene
from paper.primitives import Circle

class TestCircle(Scene):
    def __init__(self,winsz):
        Scene.__init__(self,winsz)
        self.circle1 = Circle(600,200,50,N=5,r=255,g=0,b=0)

        self.N = 5
        self.timer = 0
        self.timerMax = 10
    def draw(self):
        self.circle1.draw()

    def update(self, dt):
        #Scale circle up in a cycle
        if self.timer < self.timerMax:
            self.timer = self.timer + 1
        else:
            if self.circle1.getNVerts() < 30:
                self.circle1.setNVerts(self.N)
                self.N = self.N + 1
            else:
                self.N = 5
                self.circle1.setNVerts(self.N)
            self.timer = 0