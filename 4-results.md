---
title: Results
layout: template
filename: 4-results
--- 

# Results

Our finalized program is a videogame that uses OpenCV as the controller, has two type of AI Opponents, and is easily modified, as displayed in the image above. The red car is the Center of Mass (COM) AI, and the window in which it evaluates the road as well as the center of mass of the road are illustrated. The COM AI steers towards the red dot, the center of mass, in front of it. The green car is the line AI, and the lines it calculates are displayed, the longest of which is thicker. The Line AI steers in the direction of the longest line. Through play testing, we found that the Line AI works better and races faster than the COM AI. 

![Game Capture](http://wtrelease.github.io/Vision-Racing/PresentationLinks/Game_Capture1.png)

The OpenCV controller works well, but it does not work if one tilts their head or wears glasses. The controller responds well to the movement of people when they are in the frame, which is a third of the full camera frame, and it allows one to make very steep turns or slight turns.
