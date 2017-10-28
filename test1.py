from collections import deque
import numpy as np
import argparse
import imutils
import cv2
ap = argparse.ArgumentParser()
ap.add_argument("-v","--video",help="path to the optional video file")
args=vars(ap.parse_args())

camera = cv2.VideoCapture(0)

redLower = np.array([-10,100,100])
redUpper = np.array([5,255,255])

redLower2 = np.array([160,60,50])
redUpper2 = np.array([180,255,255])
while True:

    (grabbed, frame) = camera.read()
    if args.get('video') and not grabbed:
        break
    frame = imutils.resize(frame,width=600)
    hsv = cv2.cvtColor(frame,cv2.COLOR_BGR2HSV)
    mask = cv2.inRange(hsv,redLower,redUpper)
    mask1 = cv2.inRange(hsv,redLower2,redUpper2)
    mask = cv2.addWeighted(mask,1.0,mask1,1.0,0)
    mask = cv2.GaussianBlur(mask,(5,5),0)
    mask = cv2.dilate(mask,None,iterations=2)
    mask = cv2.erode(mask,None,iterations=2)

    circles = cv2.HoughCircles(mask,cv2.HOUGH_GRADIENT,1,20,param1=50,param2=30,minRadius=0,maxRadius=0)
    if (circles is not None):
        circles = np.round(circles[0,:].astype("int"))
        print(circles)
        for x,y,r in circles:
            cv2.circle(frame ,(x,y),r,(0,255,0),4)
    cv2.imshow("Frame",frame )
    key=cv2.waitKey(1) & 0xFF

camera.release()
cv2.destroyAllWindows()
