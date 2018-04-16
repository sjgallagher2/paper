## PAPER ##
**Python animation package for education and research (PAPER)** is an animation package written in python aimed at educational and explanatory animations. 
It can be used to animate basic primitive objects (e.g. boxes, circles, lines, arrows) as well as widgets (e.g. loading bars) in a 2D programming 
environment. This is ideal for:
* Animating sorting algorithms
* Animating neural networks
* Making simple physics simulations
* Making interactive lessons and documentation
* And more...
The possibilities are limited to your own animation. (And the primitives available to you.) With the goal of being a light-weight and easy to use package,
I've only included basic primitives and some simple widgets to get you started. The model relies on subclassing for implementing different animations. 

The animation model can be shown as follows.
* AnimationWindow
...Contains one or more scenes, responsible for calling draw and update functions for the scenes.
* Scene
...A group of primitives and/or widgets, a draw function to draw them, and an update function/state machine to control the behavior of the objects over time.  
...The order objects are drawn matters. Several scenes can be added to an animation window, and they will be drawn in the order their draw() functions are called. 
Scenes can also contain other scenes. For example, widgets are simply scenes with special functions to control them.
* Primitives
...Not actually a class, primitives are boxes, circles, lines, or arrows which maintain a set of vertices and appropriate characteristics, and provide a more or
...less common interface. Primitives are controlled within scenes. 


