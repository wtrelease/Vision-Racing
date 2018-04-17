import os, sys
import pygame
from pygame.locals import *
import random, math, numpy
import cv2
from matplotlib import pyplot as plt
from PIL import Image
from convert import convert_to_bw
from opencvcontroller import controller

class Window(object):
    """A view of the Game window"""
    def __int__(self, size):
        self.screen = pygame.display.set_mode(size)

    def draw(self):
        self.screen.blit(background, (0, 0))
        pygame.display.flip()


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


class Car(pygame.sprite.Sprite):
    """Class representing a car"""
    def __init__(self, X, Y):
        pygame.sprite.Sprite.__init__(self)
        self.orig_image = (pygame.image.load('images/car' + self.color + '.png'))
        self.rect = self.orig_image.get_rect()
        self.rect.center = (X, Y)
        self.forward_offset = self.rect.width/2 #define offset distance from the center of a car to the front
        self.side_offset = self.rect.height/2 #define offset distance from the center of a car to the side
        self.acceleration = 100 #how quickly a car will accelerate (pixels/s^2)
        self.speed_max = 300 #cars max speed (pixels/s)
        self.speed = 0 #cars initial speed
        self.rotate_speed = 0 #cars initial rotational speed
        self.rotate_speed_max = self.speed * .8 #cars initial rotational speed max
        self.rotate_speed_min = self.rotate_speed_max * .2 #cars minimum rotation speed max value
        self.bounce_speed = self.speed_max * .8 #cars rotational speed off a wall
        self.direction = 0 #cars initial direction

    """Update a cars position to the next frame"""
    def update(self, t, course):
        self.speed += self.acceleration * t #speed up car
        self.rotate_speed_max = self.speed #set max rotate speed
        if self.rotate_speed_max < self.rotate_speed_min: #keep max rotate speed above min threshold
            self.rotate_speed_max = self.rotate_speed_min
        if self.speed > self.speed_max: #keep speed under speed limit
            self.speed = self.speed_max
        self.direction += self.rotate_speed * t #turn the car
        self.direction = self.direction % 360 #simplify direction
        rads = math.radians(self.direction) #get direction in radians
        dx = int(self.speed * math.cos(rads) * t) #find x distance car should move
        dy = -int(self.speed * math.sin(rads) * t) #find y distance car should move
        self.rect.x += dx #move the car in x
        self.rect.y += dy #move the car in y
        f_x = self.forward_offset * math.cos(rads) #find x offset from center of car to front
        f_y = -self.forward_offset * math.sin(rads) #find y offset from center of car to front
        s_x = self.side_offset * math.cos(rads-math.pi/2) #find x offset from center of car to side
        s_y = -self.side_offset * math.sin(rads-math.pi/2) #find y offset from center of car to side
        left_corner = (self.rect.center[0]+f_x-s_x, self.rect.center[1]+f_y-s_y) #find coordinates of front left corner
        right_corner = (self.rect.center[0]+f_x+s_x, self.rect.center[1]+f_y+s_y) #find coordinates of front right corner
        left = (int(left_corner[0]),int(left_corner[1])) #covert left corner to int
        right = (int(right_corner[0]),int(right_corner[1])) #conver right corner to int
        if course.road[left] == 0 and course.road[self.rect.center] == 1: #check for left side collision
            self.rect.x -= dx #back up in x
            self.rect.y -= dy #back up in y
            self.speed -= self.acceleration * 5 * t #slow down
            self.direction -= self.bounce_speed * t #turn away from the wall
        elif course.road[right] == 0 and course.road[self.rect.center] == 1: #check for right side collision
            self.rect.x -= dx
            self.rect.y -= dy
            self.speed -= self.acceleration * 5 * t
            self.direction += self.bounce_speed * t
        if self.speed < 0: #prevent speed from going negative
            self.speed = 0
        self.rotate(self.direction) #call method to rotate the cars image

    """Rotate a cars image"""
    def rotate(self, direction):
        x, y = self.rect.center #store image location
        self.image = pygame.transform.rotate(self.orig_image, self.direction) #rotate image to current direction
        self.rect = self.image.get_rect() #get new image rectangle
        self.rect.center = (x, y) #move the image to origonal location

    """Set rotate speed based on steering input"""
    def steer(self, steer):
        self.rotate_speed = steer * self.rotate_speed_max #set rotate speed to speed inputs proportion of the max rotate speed

class Racer(Car):
    """Class representing a human controlled car"""
    def __init__(self, color = 'R', X=300, Y=300):
        self.color = color
        super().__init__(X,Y)

class CPU(Car):
    """Class representing a computer controlled car"""
    def __init__(self, color = 'B', X=300, Y=300):
        self.color = color
        super().__init__(X,Y)



class Controllers(object):
    pass


"""Main Function of the game"""
def race(SCREEN_WIDTH, SCREEN_HEIGHT):
    """create the games map object"""
    course = Map(SCREEN_WIDTH, SCREEN_HEIGHT)

    """Ask user to load or select a map"""
    select = input('Would you like to capture a new map? (y/n)  ')
    if select == 'y':
        new_name = input('What will you call it?  ')
        course.capture(new_name)
    print('Available maps:')
    print(os.listdir('maps/images/'))
    map_name = input('What Map Would you like?  ')
    if not os.path.isfile('maps/b&w/'+ map_name + '.png'): #if image doesn't exist in black and white create a black and white image
        convert_to_bw(map_name)
    course.build(map_name) #build course from map image


    """Initialize PyGame"""
    pygame.init()
    time = pygame.time.Clock() #create a game timer

    pygame.font.init()
    font = pygame.font.Font(None, 36)
    pygame.key.set_repeat(0, 30)

    """Create the Window"""
    screen = pygame.display.set_mode((SCREEN_WIDTH, SCREEN_HEIGHT))

    """Create the background"""
    background = pygame.image.load('maps/images/'+ map_name +'.png').convert()

    """Intitialize the cars"""
    car_list = pygame.sprite.Group()
    racer = Racer('B', 100, 100)
    car_list.add(racer)

    """Main Loop of the Game"""
    Running = True
    while Running:
        """Keep track of time"""
        time.tick(80)
        frame_time = time.get_time() / 1000 #find frame time in seconds

        """Check for key inputs inputs"""
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                sys.exit()
            elif event.type == pygame.KEYDOWN:
                if event.key == pygame.K_q:
                    sys.exit()
                if event.key == pygame.K_LEFT:
                    racer.steer(1)
                elif event.key == pygame.K_RIGHT:
                    racer.steer(-1)
            else:
                racer.steer(0)

        """Get player control input"""


        """Get CPU control input"""


        """Update the cars"""
        [car.update(frame_time, course) for car in car_list] #update all the cars positins


        """Check for events"""


        """Draw the game"""
        screen.blit(background, (0, 0))
        car_list.draw(screen)
        fps = font.render("FPS: %.2f" % time.get_fps(), 1, (255, 0, 0))
        fpspos = fps.get_rect(centerx= 80, centery = 50)
        screen.blit(fps, fpspos)
        pygame.display.flip()


if __name__ == "__main__":
    # MainWindow = RunRunMain()
    # MainWindow.MainLoop()
    race(SCREEN_WIDTH = 1280, SCREEN_HEIGHT = 720)
