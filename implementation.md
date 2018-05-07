---
title: Implementation
layout: template
filename: implementation
--- 

# Implementation

### OpenCV

##### Game Controller
We are using OpenCV as the main game input for the human player to steer the car, accomplished using facial tracking. We locate the users face with the webcam, OpenCV, and Haar Cascades-- and then translate its horizontal location into steering input. The result of this is steering that roughly tracks the user leaning from side to side, requiring full body engagement to play properly.

### AI Programs to Race Against
We have implemented a few different AI programs to controll cars automatically, each with a different method of analyzing the map around a car and determining what steering action the car should take. Our code is structured in such a way that many cars can be created, and each can "request" steering input from any AI program, allowing us to have many AI players with different methods racing at once

##### Longest Path
This is an AI method in which the car will look down the road at a few different angles, and determine which direction has the longest stretch of road before colliding with a wall. It will then instruct the car to steer towards that line, resulting in a car that always tries to aim itself as far down the road as it can see.

##### COM of Road
COM (or Center of Mass) of road is another AI method which also aims down the road but using a slightly different method. COM looks at a window of road in front of a car, and finds the average location of all the road in this window, and then steers towards this point more or less depending on how far to the side and how far in front of the car the point is.

### Architecture Diagram
![Diagram]({{https://github.com/wtrelease/Vision-Racing/blob/gh-pages/Presentation%20Links/softdesArchitecture.png}})

### Data Structures


### Use of PyGame
We utilized the pygame module for this project, mostly for animation but also to manage some keyboard inputs as well as to store game objects such as cars or potentially obstacles down the line. While not critical, this module gives us a great amount of flexibility in how we choose to look and and react to collisions between game objects.
