# animation.py
# Sam Gallagher
# 11 April 2018

# Window class for animation with Pyglet

import pyglet as pg 
import os

class AnimationWindow(pg.window.Window):
    def __init__(self, dosave=False,filename="animation",*args, **kwargs):
        super(AnimationWindow, self).__init__(*args, **kwargs)
        self.scene1 = None
        self.frame = 0
        self.dosave = dosave
        self.filename = filename


    def on_draw(self):
        self.clear()
        #self.scene1.draw()

    def update(self,dt):
        pass
        #self.scene1.update(dt)
    def saveframe(self):
        cwd = os.getcwd()
        if "Animations" not in os.listdir(cwd):
            os.mkdir("Animations")

        num = str(self.frame).zfill(5)
        fstr = "Animations/frame" + num + "-" + self.filename + ".png"
        pg.image.get_buffer_manager().get_color_buffer().save(fstr)
        self.frame = self.frame + 1

    def saveAnimation(self):
        # Save the PNGs to a single MPG4
        # Requires ffpmeg
        cwd = os.getcwd()
        if "Animations" in os.listdir(cwd) and len(os.listdir(cwd + "/Animations/")) > 0:
            os.system("ffmpeg -framerate 24 -i Animations/frame%05d-" + self.filename + ".png Animations/" + self.filename + ".mp4 -r 24")
            # Input framerate is 120 fps, output framerate is 30fps
            
            # Now clean those pngs up
            os.system("rm Animations/*.png")


class Scene(object):
    def __init__(self, winsz):
        #Window size
        self.sz_ = winsz
        self.state_ = "init"
        self.deltat = 0.0

    def draw(self):
        # Draw all objects
        pass
    def update(self,dt):
        # Handle/define scene states
        if self.state_ == "init":
            self.state_ = "init"