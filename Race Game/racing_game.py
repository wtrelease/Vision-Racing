import os, sys
import pygame
from pygame.locals import *
from helpers import *
import random
import math
import time
import cv2
import numpy
from matplotlib import pyplot as plt
from PIL import Image

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

    def capture(self):
        cap = cv2.VideoCapture(0)
        while(True):
            ret, frame = cap.read()
            cv2.imshow('frame', frame)
            if cv2.waitKey(1) & 0xFF == ord('q'):
                break
            elif cv2.waitKey(1) & 0xFF == ord('c'):
                cv2.imwrite('Capture.png', frame)
                break

        cap.release()
        cv2.destroyAllWindows()
        im_gray = cv2.imread('Capture.png', 0)
        im_bw = cv2.threshold(im_gray, 120, 255, cv2.THRESH_BINARY)[1]
        cv2.imwrite('bw_image.png', im_bw)

    def build(self):
        im_bw = cv2.imread('bw_image.png', 0)
        print(im_bw.size)
        for X in im_bw:
            for Y in X:
                pass

        plt.imshow(self.road, interpolation='nearest')
        plt.show()


class Car(pygame.sprite.Sprite):
    """Class representing a car"""
    def __init__(self):
        super().__init__()
        pygame.sprite.Sprite.__init__(self)
        self.acceleration = .1
        self.speed_max = .3
        self.rotate_speed_max = self.speed_max / 2
        self.speed = 1
        self.rotate_speed = 0
        self.direction = 0

    def update(self, t):
        self.speed += self.acceleration * t
        if self.speed > self.speed_max:
            self.speed = self.speed_max
        self.direction += self.rotate_speed * t
        self.direction = self.direction % 360
        rads = math.radians(self.direction)
        dx = int(self.speed * math.cos(rads) * t)
        dy = -int(self.speed * math.sin(rads) * t)
        self.rect.x += dx
        self.rect.y += dy
        self.rotate(self.direction)


    def rotate(self, direction):
        x, y = self.rect.center
        self.image = pygame.transform.rotate(self.orig_image, self.direction)
        self.rect = self.image.get_rect()
        self.rect.center = (x, y)

    def steer(self, steer):
        self.rotate_speed = steer * self.rotate_speed_max

class Racer(Car):
    def __init__(self, color = 'R', X=300, Y=300):
        super().__init__()
        self.orig_image = (pygame.image.load('images/car' + color + '.png'))
        self.rect = self.orig_image.get_rect()
        self.rect.center = (X, Y)

class CPU(Car):
    def __init__(self, color = 'B', X=300, Y=300):
        super().__init__()
        self.orig_image = (pygame.image.load('images/car' + color + '.png'))
        self.rect = self.orig_image.get_rect()
        self.rect.center = (X, Y)


class Controllers(object):
    pass


def race(SCREEN_WIDTH, SCREEN_HEIGHT):
    """Capture a map"""
    course = Map(SCREEN_WIDTH, SCREEN_HEIGHT)
    #course.capture()
    #course.build()


    """Initialize PyGame"""
    pygame.init()
    time = pygame.time.Clock()

    pygame.font.init()
    font = pygame.font.Font(None, 36)

    """Create the Window"""
    screen = pygame.display.set_mode((SCREEN_WIDTH, SCREEN_HEIGHT))

    """Create the background"""
    background = pygame.Surface(screen.get_size())
    background = background.convert()
    background.fill((0,0,0))

    """Intitialize the cars"""
    car_list = pygame.sprite.Group()
    racer = Racer('B')
    car_list.add(racer)

    """This is the Main Loop of the Game"""
    pygame.key.set_repeat(0, 30)

    Running = True
    while Running:
        """Keep track of time"""
        time.tick(60)
        frame_time = time.get_time()

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
        [car.update(frame_time) for car in car_list]


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
