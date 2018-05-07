import math
import pygame
from pygame.locals import *

def COM(car, road, screen, font, draw = False):

    window_width = 140
    window_length = 120
    step_size = 10

    X = car.rect.center[0]
    Y = car.rect.center[1]
    theta = math.radians(car.direction)

    road_width = road.shape[0]
    road_height = road.shape[1]

    mean_x = 0
    mean_y = 0
    count = .000000001

    for S in range(-window_width//2, window_width//2, step_size):
        for F in range(0, window_length, step_size):
            f_x = (F + car.forward_offset) * math.cos(theta) #find x offset from center of car to front
            f_y = -(F + car.forward_offset) * math.sin(theta) #find y offset from center of car to front
            s_x = S * math.cos(theta-math.pi/2) #find x offset from center of car to side
            s_y = -S * math.sin(theta-math.pi/2) #find y offset from center of car to side
            point = (X+f_x-s_x, Y+f_y-s_y) #find coordinates of front left corner
            int_point = (int(point[0]),int(point[1])) #covert left corner to int
            if point[0] >= 0 and point[0] < road_width and point[1] >= 0 and point[1] < road_height and road[int_point] == 1:
                mean_x += point[0]
                mean_y += point[1]
                count += 1
                if draw:
                    pygame.draw.circle(screen, (150, 0, 0), int_point, 2)
    COM = [int(mean_x/count), int(mean_y/count)]

    if draw:
        offset_x = car.forward_offset * math.cos(theta)
        offset_y = -car.forward_offset * math.sin(theta)
        f_x = window_length * math.cos(theta) #find x offset from center of car to front
        f_y = -window_length * math.sin(theta) #find y offset from center of car to front
        s_x = window_width/2 * math.cos(theta-math.pi/2) #find x offset from center of car to side
        s_y = -window_width/2 * math.sin(theta-math.pi/2) #find y offset from center of car to side

        FL = (X+f_x-s_x+offset_x, Y+f_y-s_y+offset_y) #find coordinates of front left corner
        FR = (X+f_x+s_x+offset_x, Y+f_y+s_y+offset_y) #find coordinates of front right corner
        BL = (X-s_x+offset_x, Y-s_y+offset_y) #find coordinates of front left corner
        BR = (X+s_x+offset_x, Y+s_y+offset_y) #find coordinates of front right corner
        FL = (int(FL[0]),int(FL[1])) #covert left corner to int
        FR = (int(FR[0]),int(FR[1])) #covert left corner to int
        BL = (int(BL[0]),int(BL[1])) #covert left corner to int
        BR = (int(BR[0]),int(BR[1])) #covert left corner to int

        pygame.draw.line(screen, (255, 0, 0), FL, FR, 2)
        pygame.draw.line(screen, (255, 0, 0), FL, BL, 2)
        pygame.draw.line(screen, (255, 0, 0), BR, FR, 2)
        pygame.draw.line(screen, (255, 0, 0), BL, BR, 2)
        pygame.draw.circle(screen, (255, 0, 0), COM, 5)

    COM_angle = -math.degrees(math.atan2(COM[1]-Y, COM[0]-X))
    COM_angle += 360
    angle_diff = COM_angle - car.direction
    angle_diff = angle_diff % 360

    if angle_diff > 180:
        angle_diff -= 360

    COM_dist = ((COM[1]-Y)**2 + (COM[0]-X)**2)**.5
    COM_diff = math.sin(math.radians(angle_diff))*COM_dist

    angle_range = 45
    sweep_range = 45

    if angle_diff > angle_range:
        angle_diff = angle_range
    elif angle_diff < -angle_range:
        angle_diff = -angle_range

    if COM_diff > sweep_range:
        COM_diff = sweep_range
    elif COM_diff < -sweep_range:
        COM_diff = -sweep_range

    steer = angle_diff/angle_range
    steer = COM_diff/sweep_range


    return steer
