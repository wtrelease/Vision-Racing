import numpy as np
from collections import deque
import cv2
import cv2.aruco as aruco
import os
import glob
import math
import sys

def controller(cap,old_turn):
    """Aruco Marker controller that tracks the orientation of the Marker
    and uses the angle to steer"""
    # Capture frame by frame
    ret, frame = cap.read()
    gray = cv2.cvtColor(frame, cv2.COLOR_BGR2GRAY)
    aruco_dict = aruco.Dictionary_get(aruco.DICT_6X6_250)
    parameters = aruco.DetectorParameters_create()
    #Lists of ids and the corners belonging to each id
    corners, ids, rejectedImgPoints = aruco.detectMarkers(gray, aruco_dict,
        parameters=parameters)
    #print(corners)
    for tag in corners: #Tracks the angle of two corners to controller steering
        TL = tag[0][0] #Position of top left corner
        BL = tag[0][3] #Position of bottom left corner
        dx = TL[0]-BL[0] #Change in x-positions of the two corners
        dy = TL[1]-BL[1] #Change in y-positions of the two corners
        angle = math.atan(dx/dy) #Angle tracked to tell whether to turn left or right
        return (angle*180/math.pi)/90 #Returns angle between the corners
    #Marker detection, uses gray(the frame) to follow the Marker
    gray = aruco.drawDetectedMarkers(gray, corners)
    #Display the resulting frame
    #cv2.imshow('frame', gray)
    # if cv2.waitKey(1) & 0xFF == ord('q'):
    #     cap.release()
    #     cv2.destroyAllWindows
    #     break
    return old_turn

#Defining the facial recognition haarcascade
face_cascade = cv2.CascadeClassifier('haarcascade_frontalface_alt.xml')

def face_controller(cap, out, steer, record = False):
    """Face Controller that tracks the x-position of ones faces
    within an exponential function and records the player as they play"""
    ret, frame = cap.read()
    gray = cv2.cvtColor(frame, cv2.COLOR_BGR2GRAY)
    frame_width = cap.get(3) #Determines the width of the camera frame in pixels
    frame_height = int(cap.get(4)) #Determines the height of camera frame in pixels
    faces = face_cascade.detectMultiScale(gray,
                                        scaleFactor=1.1,
                                        minNeighbors=5,
                                        minSize=(30, 30))
    for (x, y, w, h) in faces:
        face_center = x + w/2 #Sets the center of the face frame
        frame_center = frame_width/2 #Sets the center of camera frame
        bounds = .3 #Limits how far of each side of the frame to keep track of
        upper_bound = frame_width*(1-bounds) #Maximum value tracker follows
        lower_bound = frame_width*bounds #Minimum value tracker follows
        view_range = upper_bound - lower_bound #Sets size of the frame being accounted for
        if face_center < lower_bound: #Makes sure the player face does not go out of bounds
            face_center = lower_bound
        if face_center > upper_bound:
            face_center = upper_bound
        steer = (face_center - frame_center)/view_range*2 #Sets the steer value using location on frame
        power = 2.6 #Exponent for steer
        steer = abs(steer)**(power-1)*steer #Uses steer to set the sensitivity of the steering as a function of position
        if record: #Records what the camera sees and write rectangle around the perosns face and line at the center of their face
            cv2.rectangle(frame, (x, y), (x+w, y+h), (0, 255, 255))
            line_loc = int(frame_center + view_range/2*steer)
            cv2.line(frame, (line_loc, frame_height), (line_loc, frame_height - 50), (0, 255, 255), 3)
            # cv2.imshow('frame', frame)
        # if cv2.waitKey(1) & 0xFF == ord('q'):
        #     cv2.destroyAllWindows
        #     break
    if record:
        out.write(frame)
    return steer
