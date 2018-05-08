import os, sys
import pygame
from pygame.locals import *
import random, math, numpy
import cv2
import numpy as np
from matplotlib import pyplot as plt
from PIL import Image
from convert import convert_to_bw
from opencvcontroller import controller, face_controller
from LINE_AI import Line
from COM_AI import COM
from pygame.font import *

class Map(object):
    """Class representing a game map"""
    def __init__(self,width,height):
        self.road = numpy.zeros((width, height), numpy.int8)
        self.width = width
        self.height = height

    """Capture an image from the webcam for use as a map"""
    def capture(self, name = 'Capture'):
        cap = cv2.VideoCapture(0)
        while(True):
            ret, frame = cap.read()
            cv2.rectangle(frame, (0, 0), (self.width, self.height), (0, 0, 255))
            cv2.imshow('frame', frame)
            if cv2.waitKey(1) & 0xFF == ord('c'):
                ret, frame = cap.read()
                cv2.imwrite('maps/images/'+ name + '.png', frame)
                break
            elif cv2.waitKey(1) & 0xFF == ord('q'):
                break

        cap.release()
        cv2.destroyAllWindows()
        #Convert to a binary black and white image
        convert_to_bw(name)

    """Build the map matrix from the black and white map image"""
    def build(self, name):
        im_bw = Image.open('maps/b&w/'+ name +'.png')
        width, height = im_bw.size
        for x in range(self.width):
            for y in range(self.height):
                if x < width and y < height:
                    if im_bw.getpixel((x,y)) == 0:
                        self.road[x,y] = 1

        self.finish_line_bottom = [width//4, height-1]
        while self.road[self.finish_line_bottom[0], self.finish_line_bottom[1]] == 0:
            self.finish_line_bottom[1] -= 1
        self.finish_line_top = list(self.finish_line_bottom)
        while self.road[self.finish_line_top[0], self.finish_line_top[1]] == 1:
            self.finish_line_top[1] -= 1
        self.finish_line_top[1] += 1

        self.start_X = width//4 - 40
        self.start_Y = (self.finish_line_top[1] + self.finish_line_bottom[1])/2

        #plt.imshow(self.road, interpolation='nearest')
        #plt.show()

class Car(pygame.sprite.Sprite):
    """Class representing a car"""
    def __init__(self, name, X, Y):
        pygame.sprite.Sprite.__init__(self)
        self.orig_image = (pygame.image.load('images/car' + self.color + '.png'))
        self.name = name
        self.rect = self.orig_image.get_rect()
        self.rect.center = (X, Y)
        self.location_X = X
        self.location_Y = Y
        self.forward_offset = self.rect.width/2 #define offset distance from the center of a car to the front
        self.side_offset = self.rect.height/2 #define offset distance from the center of a car to the side
        self.acceleration = 50 #how quickly a car will accelerate (pixels/s^2)
        self.brake_accel = 250
        self.speed_max = 200 #cars max speed (pixels/s)
        self.speed = 0 #cars initial speed
        self.rotate_speed = 0 #cars initial rotational speed
        self.rotate_speed_max = 0 #cars initial rotational speed max
        self.rotate_speed_max_coeff = 1
        self.bounce_speed = self.speed_max * .8 #cars rotational speed off a wall
        self.direction = 0 #cars initial direction
        self.lap_primer = 0
        self.crossed = 0
        self.lap_count = 0

    """Update a cars position to the next frame"""
    def update(self, t, course):
        self.speed += self.acceleration * t #speed up car
        self.rotate_speed_max = self.speed * self.rotate_speed_max_coeff #set max rotate speed
        if self.speed > self.speed_max: #keep speed under speed limit
            self.speed = self.speed_max
        self.direction += self.rotate_speed * t #turn the car
        self.direction = self.direction % 360 #simplify direction
        rads = math.radians(self.direction) #get direction in radians
        dx = self.speed * math.cos(rads) * t #find x distance car should move
        dy = -self.speed * math.sin(rads) * t #find y distance car should move
        self.location_X += dx #move the car in x
        self.location_Y += dy #move the car in y
        collide = self.collision(t, course, rads)
        if collide:
            self.location_X -= dx #move the car in x
            self.location_Y -= dy #move the car in y
        if self.speed < -self.speed_max/3: #prevent speed from going negative
            self.speed = -self.speed_max/3
        self.rect.x = int(self.location_X)
        self.rect.y = int(self.location_Y)
        self.rotate() #call method to rotate the cars image
        self.laps(course)

    """Check for Finish Line Crossing"""
    def laps(self, course):
        if self.lap_primer == 0 and self.rect.y < course.road.shape[1]/3:
            self.lap_primer = 1
            self.crossed = 0
        elif self.crossed == 0 and self.lap_primer == 1 and self.rect.y > course.finish_line_top[1] and self.rect.x > course.finish_line_top[0]:
            self.crossed = 1
            self.lap_count += 1
            self.lap_primer = 0

    """Check for Car Collision"""
    def collision(self, t, course, rads):
        collide = False
        f_x = self.forward_offset * math.cos(rads) #find x offset from center of car to front
        f_y = -self.forward_offset * math.sin(rads) #find y offset from center of car to front
        s_x = self.side_offset * math.cos(rads-math.pi/2) #find x offset from center of car to side
        s_y = -self.side_offset * math.sin(rads-math.pi/2) #find y offset from center of car to side
        left_corner = (self.location_X+f_x-s_x, self.location_Y+f_y-s_y) #find coordinates of front left corner
        right_corner = (self.location_X+f_x+s_x, self.location_Y+f_y+s_y) #find coordinates of front right corner
        left = (int(left_corner[0]),int(left_corner[1])) #covert left corner to int
        right = (int(right_corner[0]),int(right_corner[1])) #convert right corner to int
        if course.road[left] == 0 and course.road[self.rect.center] == 1: #check for left side collision
            collide = True
            self.speed -= self.brake_accel * t #slow down
            self.direction -= self.bounce_speed * t #turn away from the wall
        elif course.road[right] == 0 and course.road[self.rect.center] == 1: #check for right side collision
            collide = True
            self.speed -= self.brake_accel * t
            self.direction += self.bounce_speed * t
        return collide

    """Rotate a cars image"""
    def rotate(self):
        self.image = pygame.transform.rotate(self.orig_image, self.direction) #rotate image to current direction
        self.rect = self.image.get_rect() #get new image rectangle
        self.rect.center = (self.location_X, self.location_Y) #move the image to origonal location

    """Set rotate speed based on steering input"""
    def steer(self, steer, t):
        self.rotate_speed = steer * self.rotate_speed_max #set rotate speed to speed inputs proportion of the max rotate speed
        self.speed -= self.acceleration * t * abs(steer)**4 / 75 * self.speed #speed up car

class Racer(Car):
    """Class representing a human controlled car"""
    def __init__(self, name, color = 'R', X=300, Y=300):
        self.color = color
        super().__init__(name, X, Y)
        self.rotate_speed_max_coeff = .8

class CPU(Car):
    """Class representing a computer controlled car"""
    def __init__(self, name, speed = 150, accel = 35, color = 'B', X=300, Y=300):
        self.color = color
        super().__init__(name, X, Y)
        self.acceleration = accel
        self.speed_max = speed

def start_screen(screen_width, screen_height):
    """Main menu"""
    #screen
    screen = pygame.display.set_mode((screen_width, screen_height))
    #screen.display.set_caption('ROAD RAGE')
    screen.fill(pygame.Color(0,200,130))

    #title display
    title_font = pygame.font.SysFont('Arial', 80)
    title_surf = title_font.render('Vision Racing', True, (0,0,0))

    #slogan display
    slogan_font = pygame.font.SysFont('Arial', 60)
    instruction_surf1 = slogan_font.render('Race With Your Face',True,(0,0,0))

    #intruction display
    instruction_font = pygame.font.SysFont('Arial', 40)
    instruction_surf2 = instruction_font.render('Press SPACE to start, or Esc to quit.',True,(0,0,0))


    #menu loop with all of the information displayed
    running = True
    while running:
        screen.blit(title_surf, ((screen_width/2) - 250,300))
        screen.blit(instruction_surf1, ((screen_width/2) - 275,400))
        screen.blit(instruction_surf2, ((screen_width/2) - 310,750))
        #checks for space or escape clicks
        for event in pygame.event.get():
            if event.type == KEYDOWN:
                if event.key == pygame.K_ESCAPE:
                    sys.exit()
                #move to main loop if space is pressed
                if event.key == pygame.K_SPACE:
                    running = False
            if event.type == QUIT:
                sys.exit()
        pygame.display.update()


"""Main Function of the game"""
def race():
    """Ask user to load or select a map"""
    if False:
        select = input('Would you like to capture a new map? (y/n)  ')
        if select == 'y':
            new_name = input('What will you call it?  ')
            course.capture(new_name)
        print('Available maps:')
        print(os.listdir('maps/images/'))
        map_name = input('What Map Would you like?  ')
    else:
        map_name = 'course'
    if not os.path.isfile('maps/b&w/'+ map_name + '.png'): #if image doesn't exist in black and white create a black and white image
        convert_to_bw(map_name)

    """Create the background"""
    background_image = pygame.image.load('maps/images/'+ map_name +'.png')

    """Create the map"""
    screen_width, screen_height = background_image.get_size()
    course = Map(screen_width, screen_height)
    course.build(map_name) #build course from map image

    """Create start screen"""
    pygame.font.init() # initialize the font
    start_screen(screen_width, screen_height)

    """Initialize PyGame"""
    pygame.init()
    time = pygame.time.Clock() #create a game timer

    pygame.font.init()
    font = pygame.font.Font(None, 36)
    pygame.key.set_repeat(0, 30)

    """Create the Window"""
    screen = pygame.display.set_mode((screen_width, screen_height))
    background = background_image.convert()

    """Intitialize the cars"""
    car_list = pygame.sprite.Group()
    COM_AI_list = pygame.sprite.Group()
    LINE_AI_list = pygame.sprite.Group()
    racer = Racer('Player', 'B', course.start_X, course.start_Y)
    CPU1 = CPU('Fast Line AI', 160, 20, 'R', course.start_X, course.start_Y+15)
    CPU2 = CPU('Quick Line AI', 145, 60, 'G', course.start_X, course.start_Y-15)
    car_list.add(racer)
    car_list.add(CPU1)
    car_list.add(CPU2)
    LINE_AI_list.add(CPU1)
    LINE_AI_list.add(CPU2)

    """Initialize the webcam"""
    cap = cv2.VideoCapture(0)
    cap_width = int(cap.get(3))
    cap_height = int(cap.get(4))
    turn = 0
    input_time = 0
    input_frequency = 20
    fourcc = cv2.VideoWriter_fourcc('M','J','P','G')
    out = cv2.VideoWriter('gameplay.avi',fourcc, input_frequency, (cap_width,cap_height))

    """Main Loop of the Game"""
    Running = True
    time.tick()
    while Running:
        """Keep track of time"""
        time.tick(40)
        frame_time = time.get_time() / 1000 #find frame time in seconds
        input_time += frame_time
        """Check for key inputs inputs"""
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                sys.exit()
            elif event.type == pygame.KEYDOWN:
                if event.key == pygame.K_q:
                    sys.exit()
            #     if event.key == pygame.K_LEFT:
            #         racerTurn = 1
            #     elif event.key == pygame.K_RIGHT:
            #         racerTurn = -1
            # else:
            #     racerTurn = 0

        # racer.steer(racerTurn, frame_time)

        """Get player control input"""
        # turn = controller(cap, turn)
        # racer.steer(-turn)

        """Get plater control input through face recognition"""
        if input_time > 1/input_frequency and True:
            turn = face_controller(cap, out, turn, True)
            input_time = 0
        racer.steer(turn, frame_time)

        """Draw Game Map"""
        screen.blit(background, (0, 0))
        pygame.draw.line(screen, (255, 255, 0), course.finish_line_top, course.finish_line_bottom, 4)
        pygame.draw.line(screen, (0, 0, 0), (0, 80), (screen_width, 80), 180)

        """Get CPU control input"""
        [car.steer(COM(car, course.road, screen, font), frame_time) for car in COM_AI_list]
        [car.steer(Line(car, course.road, screen, font), frame_time) for car in LINE_AI_list]

        """Update the cars"""
        [car.update(frame_time, course) for car in car_list] #update all the cars positins

        """Check for events"""

        """Draw the game"""
        car_list.draw(screen)
        fps = font.render("FPS: %.2f" % time.get_fps(), 1, (255, 0, 0))
        screen.blit(fps, [30, 20])
        lap = font.render("Lap Count", 1, (255, 0, 0))
        screen.blit(lap, [screen_width - 160, 20])
        car_track = 0
        for car in car_list:
            car_track += 1
            lap = font.render(car.name + ": %.1f" % car.lap_count, 1, (255, 0, 0))
            screen.blit(lap, [screen_width - 210 * (len(car_list) + 1 - car_track), 60])
        pygame.display.flip()

    cap.release()
    out.release()
    cv2.destroyAllWindows()




if __name__ == "__main__":
    # MainWindow = RunRunMain()
    # MainWindow.MainLoop()
    race()
