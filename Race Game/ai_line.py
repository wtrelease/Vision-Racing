import math
import pygame

def AI_line(car, road, screen):
    thetas = range(-90, 90, 1)


    x = car.rect.center[0]
    y = car.rect.center[1]
    step = 1
    check_offset = 16


    max_distance = 0
    best_angle = 0
    best_point = [0, 0]
    for theta_offset in thetas:
        theta = car.direction + theta_offset
        rads = math.radians(theta)
        direction = math.radians(car.direction)
        on_road = True
        s_x = check_offset * math.cos(direction-math.pi/2) #find x offset from center of car to side
        s_y = -check_offset * math.sin(direction-math.pi/2) #find y offset from center of car to side
        left = [x-s_x, y-s_y] #find coordinates of front left corner
        right = [x+s_x, y+s_y]

        pygame.draw.circle(screen, (255, 0, 0), [int(left[0]),int(left[1])], 4)
        pygame.draw.circle(screen, (0, 255, 0), [int(right[0]),int(right[1])], 4)
        distance = 0
        x_step = math.cos(rads)*step
        y_step = -math.sin(rads)*step
        while on_road:
            distance += step
            left[0] += x_step
            left[1] += y_step
            right[0] += x_step
            right[1] += y_step

            if road[int(left[0]),int(left[1])] == 0 or road[int(right[0]),int(right[1])] == 0:
                on_road = False
        # if theta_offset == 0:
        #     pygame.draw.line(screen, (255, 0, 0), [car.rect.centerx, car.rect.centery], [x, y])
        #     print(theta)
        #     print(distance)
        if distance > max_distance:
            max_distance = distance
            best_angle = theta
            best_point = [(left[0]+right[0])/2,(left[1]+right[1])/2]

    pygame.draw.line(screen, (255, 0, 0), [car.rect.centerx, car.rect.centery], best_point)


    angle_diff = best_angle - car.direction
    if angle_diff > 60:
        steer = 1
    elif angle_diff < -60:
        steer = -1
    else:
        steer = angle_diff/60

    if max_distance == 0:
        steer = 0

    return steer
