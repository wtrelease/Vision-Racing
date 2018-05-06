import numpy as np
from collections import deque
import cv2
import cv2.aruco as aruco
import os
import glob
import math
import sys

def controller(cap,old_turn):

    #while True:
    # Capture frame by frame
    ret, frame = cap.read()
    #print(from shape) 480x640
    gray = cv2.cvtColor(frame, cv2.COLOR_BGR2GRAY)
    aruco_dict = aruco.Dictionary_get(aruco.DICT_6X6_250)
    parameters = aruco.DetectorParameters_create()
    #print(parameters)
            #Lists of ids and the corners belonging to each id
    corners, ids, rejectedImgPoints = aruco.detectMarkers(gray, aruco_dict,
        parameters=parameters)
    #print(corners)
    for tag in corners:
        TL = tag[0][0]
        BL = tag[0][3]
        dx = TL[0]-BL[0]
        dy = TL[1]-BL[1]
        angle = math.atan(dx/dy)
        return (angle*180/math.pi)/90
    gray = aruco.drawDetectedMarkers(gray, corners)
            #print(rejectedImgPoints)
    #Display the resulting frame
    #cv2.imshow('frame', gray)
    # if cv2.waitKey(1) & 0xFF == ord('q'):
    #     cap.release()
    #     cv2.destroyAllWindows
    #     break
    return old_turn


face_cascade = cv2.CascadeClassifier('haarcascade_frontalface_alt.xml')

def face_controller(cap,steer):
    ret, frame = cap.read()
    gray = cv2.cvtColor(frame, cv2.COLOR_BGR2GRAY)
    frame_width = cap.get(3)
    faces = face_cascade.detectMultiScale(gray,
                                        scaleFactor=1.1,
                                        minNeighbors=5,
                                        minSize=(30, 30))
    for (x, y, w, h) in faces:
        cv2.rectangle(frame, (x,y), (x+w, y+h), (0, 255, 0), 2)
        face_center = x + w/2
        frame_center = frame_width/2
        bounds = .3
        upper_bound = frame_width*(1-bounds)
        lower_bound = frame_width*bounds
        view_range = upper_bound - lower_bound
        if face_center < lower_bound:
            face_center = lower_bound
        if face_center > upper_bound:
            face_center = upper_bound
        steer = (face_center - frame_center)/view_range*2
        # cv2.rectangle(gray, (x, y), (x+w, y+h), (0, 0, 255))
        # cv2.imshow('frame', gray)
        # if cv2.waitKey(1) & 0xFF == ord('q'):
        #     cv2.destroyAllWindows
        #     break
    power = 2.2
    return abs(steer)**(power-1)*steer
