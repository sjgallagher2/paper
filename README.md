## PAPER ##
**Python animation package for education and research (PAPER)** is an animation package written in python aimed at educational and explanatory animations. 
It can be used to animate basic primitive objects (e.g. boxes, circles, lines, arrows) as well as widgets (e.g. loading bars) in a 2D programming 
environment. This is ideal for:
* Animating sorting algorithms
* Animating neural networks
* Making simple physics simulations
* Making interactive lessons and documentation
* And more...

The possibilities are limited to your own imagination. (And the primitives available to you.) With the goal of being a light-weight and easy to use package,
I've only included basic primitives and some simple widgets to get you started. The model relies on subclassing for implementing different animations. 

The animation model can be shown as follows.

* AnimationWindow

   Contains one or more scenes, responsible for calling draw and update functions for the scenes. 

* Scene

   A group of primitives and/or widgets, a draw function to draw them, and an update function/state machine to control the behavior of the objects over time.  
   The order in which objects are drawn matters. Several scenes can be added to an animation window, and they will be drawn in the order their draw() functions are called. 
Scenes can also contain other scenes. For example, widgets are simply scenes with special functions to control them. 
* Primitives

   Not actually a class, primitives are boxes, circles, lines, or arrows which maintain a set of vertices and appropriate characteristics, and provide a more or 
   less common interface. Primitives are controlled within scenes. 

### Simple example ###
```python
import paper
import pyglet

# Subclass the animation window for our animation
class SimpleAnimation(paper.animationwindow.AnimationWindow):
    def __init__(self, *args, **kwargs):
        # Call parent constructor
        paper.AnimationWindow.__init__(self,*args,**kwargs)
        
        # Create a scene (this one is an example from paper)
        self.scene1 = paper.scene.bouncingboxscene.BouncingBoxScene(self.get_size())
    
    # Create draw method (must be called on_draw())
    def on_draw(self):
        # Clear and draw
        self.clear()
        self.scene1.draw()
    
    # Create update method
    def update(self,dt):
        # dt is the time since the last update in seconds
        self.scene1.update(dt)

# Main animation code through Pyglet
if __name__ == "__main__":
    master = SimpleAnimation(1200,600) # You can give window size as parameters, 1200 x 600 px here
    pyglet.clock.schedule_interval(master.update, 1/120) # 120 frames per second animation
    pyglet.app.run()
```
