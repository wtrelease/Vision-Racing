import pygame
import time
import os
import random
import cv2
import numpy
import sys

class Window(object):
    """A view of the Game window"""
    def __int__(self, model, size):
        self.model = model
        self.screen = pygame.display.set_mode(size)

    def draw(self):
        pass

class Model(object):
    """Encodes a model of the game state"""
class Map(object):
    pass


class Racer(object):
    pass



class Controllers(object):
    pass


class Sprites(object):
    pass


class CPU(object):
    pass



def race():
    pygame.init()

    size = (1800, 800)
    model = Model(size)
    view = Window(model, size)
    while running:
        """Get Player Input"""


        """Update the game"""


        """Check for events"""



        """print the game"""
        pass
