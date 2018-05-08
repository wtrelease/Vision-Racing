import math
import pygame

def Line(car, road, screen, font, draw = False):
    thetas = range(-90, 90, 3) # define the angles that will be checked


    x = car.rect.center[0]  # define x and y as the coordinates of the center of the car
    y = car.rect.center[1]
    step = 5 # define the size of step taken when check for being off road
    check_offset = 16 # how far to each side of the center we're checking


    max_distance = 0 # initialize max didstance
    best_angle = 0 # initialize best angle
    best_point = [0, 0] # intialize best point
    # through the defined thetas
    for theta_offset in thetas:
        theta = car.direction + theta_offset # add the angle we want to check to car's current direction
        rads = math.radians(theta) # convert theta to radians
        direction = math.radians(car.direction) # convert car direction to radians
        on_road = True # initialize on_road as True
        s_x = check_offset * math.cos(direction-math.pi/2) #find x offset from center of car to side
        s_y = -check_offset * math.sin(direction-math.pi/2) #find y offset from center of car to side
        left = [x-s_x, y-s_y] #find coordinates of front left corner
        right = [x+s_x, y+s_y]
        if draw:
            # illustrate the two points from which it is checking lines
            pygame.draw.circle(screen, (255, 0, 0), [int(left[0]),int(left[1])], 4)
            pygame.draw.circle(screen, (0, 255, 0), [int(right[0]),int(right[1])], 4)
        distance = 0 # initialize distance
        x_step = math.cos(rads)*step # define the step size in the x direction
        y_step = -math.sin(rads)*step # define the step size in the y direction
        while on_road:
            distance += step # increase distance by each step
            left[0] += x_step # increase the left point's x value by each x_step
            left[1] += y_step # increase the left point's y value by each y_step
            right[0] += x_step # increase the right point's x value by each x_step
            right[1] += y_step # increase the right point's y value by each y_step

            if road[int(left[0]),int(left[1])] == 0 or road[int(right[0]),int(right[1])] == 0: # if the new point is off road
                on_road = False # end while loop
                distance -= step # save distance as the last distance while on road
            if draw:
                # illustrate the lines being checked
                pygame.draw.line(screen, (150, 0, 0), [car.rect.centerx, car.rect.centery], ((left[0]+right[0])/2,(left[1]+right[1])/2), 2)

        if distance > max_distance: # if the new distance is bigger than max_distance
            max_distance = distance # redefine max_distance as the new distance
            best_angle = theta # redefine best_angle as the current theta
            best_point = [(left[0]+right[0])/2,(left[1]+right[1])/2] # redefine best_point as the current point

    if draw:
        # redraw only the line to the best point so that it is noticably different from the other lines
        pygame.draw.line(screen, (255, 0, 0), [car.rect.centerx, car.rect.centery], best_point, 2)


    angle_diff = best_angle - car.direction # angle the car needs to turn
    # if angle_diff is > 60 or < -60, steer will be at the max or min
    if angle_diff > 60:
        steer = 1
    elif angle_diff < -60:
        steer = -1
    else:
        # steer is a number between -1 and 1
        steer = angle_diff/60
    # if the car is off road, it won't steer until it is on road 
    if max_distance == 0:
        steer = 0

    return steer
