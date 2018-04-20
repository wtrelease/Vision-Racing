# Architecture Review #2

### Background and Context
We aim to create a Mario Kart style racing game which uses OpenCV for control inputs and has AI driven computer players to race against. Our MVP is a playable game in which you can navigate around a course and avoid simple obstacles. We hope to also implement AI racers to play against, and will add additional and more complex game elements as time permits.
We have a racing game that that can create new maps using OpenCV to process a drawing of a map, and uses OpenCV for basic steering control. Going forward, we plan to implement a few more aspects of the game itself, like finish line, score trackers, timers, etc., and use AI to make various types of bots to play against, and hopefully race these bots against each other and a human player.

### Key Questions

##### AI Questions:
- What would be a good way to make an AI opponent?
- Is there a way to change the difficulty of the AI?
- One idea that we have is to measure the distance from the car to the edge of the road at three angles, and steer the car in the angle with the longest distance. We would be taking and comparing these distances every time we update the game.
  - Is there a way to make this more efficient?
  - Is there a way to change the difficulty of this method?

##### OpenCV Questions:
- What is the best way to use face tracking to steer the cars?
  - Tracking coordinates of the frame, tilt of head, movement of the frame follows movement of car
- Any methods that would help to use body detection rather than just face detection?
- If body detection is used, what movements should be captured and how would I be able to capture that?
- Any recommendations on face or body detection haarcascades?

##### Center of Mass AI
- Goal is to be similar to how driver makes decisions
- Views section of map ahead of it, steers to center of mass of road
- Further to the side this is the harder it steers
- Obstacles and objectives can add steering input
- What shape should view be?
- Should parts of view have different weights?
- What problems might this have?


#### Agenda
- Go over background
- Explain code architecture
- Go over each section we have questions on and have a discussion
