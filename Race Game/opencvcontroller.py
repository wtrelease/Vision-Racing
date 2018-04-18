import numpy as np
from collections import deque
import cv2
import cv2.aruco as aruco
import os
import glob
import math

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
