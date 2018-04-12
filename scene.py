# scene.py
# Sam Gallagher
# 12 April 2018
#
# Scene interface for animations


class Scene(object):
    def __init__(self, winsz):
        #Window size
        self.sz = winsz
        self.state = "init"

    def draw(self):
        # Draw all objects
        pass
    def update(self,dt):
        # Handle/define scene states
        if self.state == "init":
            self.state = "init"