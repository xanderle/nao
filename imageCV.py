import sys
import numpy as np
import cv2
from copy import deepcopy
from naoqi import ALProxy
import argparse

ip_addr = "192.168.0.101"
port_num = 9559

# get NAOqi module proxy
videoDevice = ALProxy('ALVideoDevice', ip_addr, port_num)
motion = ALProxy("ALMotion", ip_addr, port_num)
tts = ALProxy("ALTextToSpeech", ip_addr, port_num)

global distance
distance = 0
# subscribe top camera
AL_kTopCamera = 0
AL_kQVGA = 1            # 320x240
AL_kBGRColorSpace = 13
captureDevice = videoDevice.subscribeCamera(
    "test", AL_kTopCamera, AL_kQVGA, AL_kBGRColorSpace, 10)

# create image
width = 320
height = 240
image = np.zeros((height, width, 3), np.uint8)


def feed(motionBool):
    distance = 0.030
    prevSec = ["0","0"]
    state = 'pitchalign'
    tts.say("I'm aligning with the pitch")

    width = 320
    height = 240
    image = np.zeros((height, width, 3), np.uint8)
    global distance
    while True:
        #print 'Live feed'
        # get image
        result = videoDevice.getImageRemote(captureDevice);

        if result == None:
            print 'cannot capture.'
        elif result[6] == None:
            print 'no image data string.'
        else:
            print state
            # translate value to mat
            values = map(ord, list(result[6]))
            i = 0
            for y in range(0, height):
                for x in range(0, width):
                    image.itemset((y, x, 0), values[i + 0])
                    image.itemset((y, x, 1), values[i + 1])
                    image.itemset((y, x, 2), values[i + 2])
                    i += 3

            # show image
            frame = deepcopy(image)
            if state == 'pitchAlign':
                res = alignBody(image,frame,motionBool)
                if (res == "s"):
                    state = 'ballAlign'

            direction = drawCenterOfMass(image,frame)
            print distance[0]
            print direction
            if direction == ["s","d"] and distance[0] < 700 and state != pitchAlign:
                clearBall(motion)
                state = "pitchAlign"
            else:
                cv2.line(frame,(0,height/2),(width,height/2),(0,255,0),1)
                cv2.line(frame,(width/2,0),(width/2,height),(0,255,0),1)
                cv2.imshow("Big Brother", frame)
                cv2.imwrite("file.png",frame)
                if(prevSec == ["l","d"] and direction == ["0","0"]):
                    tts.say("Dive Left")
                    print("Raise Left")
                elif(prevSec == ["r","d"] and direction == ["0","0"]):
                    tts.say("Dive Right")
                    print("Raise Right")
                # centre head on ball
                centerHead(direction)
                # move left or right for ball
                if state == 'ballAlign':
                    alignWithBall(direction, motionBool)

                if direction[0]=="s":
                    state = "pitchAlign"

                prevSec = direction

        # exit by [ESC
        if cv2.waitKey(33) == 27:
            print 'Stop Motion'
            if motionBool:
                motion.moveToward(0,0,0)
            break

    videoDevice.unsubscribe(captureDevice)

def alignWithBall(directions,motionBool):
    print directions

    angles = motion.getAngles("HeadYaw",True)
    #print angles
    if directions[0] == 'l':
        print 'Moving Left'
        if motionBool:
            motion.moveToward(0, 0.8, 0)

    elif directions[0] == 'r':
        print 'Moving Right'
        if motionBool:
            motion.moveToward(0, -0.8, 0)
    elif directions[0]=="s":
        print 'Stop Motion'
        if motionBool:
            motion.moveToward(0, 0, 0)
    else:
        print 'Stop Motion'
        if motionBool:
            motion.moveToward(0, 0, 0)

def alignBody(image,frame, motionBool):
    gray_image = cv2.cvtColor(image,cv2.COLOR_BGR2GRAY)
    #mask_white = cv2.inRange(gray_image,0,80)
    mask_white = cv2.inRange(gray_image,200,255)
    mask_image = cv2.bitwise_and(gray_image,mask_white)
    #cv2.imshow("Mask White",mask_white);
    kernel_size = 5,5
    gauss_gray = cv2.GaussianBlur(mask_image,kernel_size,0)

    low_threshold = 50
    high_threshold = 150
    canny_edges = cv2.Canny(gauss_gray,low_threshold,high_threshold)

    lines = cv2.HoughLines(canny_edges,1,np.pi/180,100)
    try:
        for rho,theta in lines[0]:
            a = np.cos(theta)
            b = np.sin(theta)
            x0 = a*rho
            y0 = b*rho
            x1 = int(x0 + 1000*(-b))
            y1 = int(y0 + 1000*(a))
            x2 = int(x0 - 1000*(-b))
            y2 = int(y0 - 1000*(a))
            cv2.line(frame,(x1,y1),(x2,y2),(0,0,255),2)
            dy = y1-y2
            #print dy
            if np.abs(dy) >= 35:
                if np.sign(dy) == 1:
                    if motionBool:
                        motion.moveToward(0,0,0.1)
                    print 'rotating Left'
                    return 'l'
                else:
                    if motionBool:
                        motion.moveToward(0,0,-0.1)
                    print 'rotating right'
                    return 'r'
            else:
                if motionBool:
                    motion.moveToward(0,0,0)
                print 'Stopping motion'
                return 's'
    except:
        return 's'

def centerHead(direction):
    angles = motion.getAngles("HeadPitch",True)
    #print(angles)

    if(direction[1]=="u" and angles[0] > 0.3):
        motion.changeAngles('HeadPitch',-0.1,0.1)
    elif(direction[1]=="d"):
        motion.changeAngles("HeadPitch",0.1,0.1)
    elif(direction[1]=="s"):
        motion.changeAngles("HeadPitch",0.0,0.1)
    #print(direction)
    #
    # if(direction[0] =='l'):
    #     motion.changeAngles('HeadYaw',0.1,0.1)
    # elif(direction[0] =='r'):
    #     motion.changeAngles('HeadYaw',-0.1,0.1)
    # elif(direction[0]=='s'):
    #     motion.changeAngles('HeadYaw',0.0,0.1)

def clearBall(motionProxy):
    motionProxy.moveTo(0.5, 0.0, 0.0)
    motionProxy.waitUntilMoveIsFinished()
    motionProxy.moveTo(-0.5, 0.0, 0.0)
    motionProxy.waitUntilMoveIsFinished()

def drawCenterOfMass(image,frame):
    height,width,channels = image.shape
    hsv = cv2.cvtColor(image, cv2.COLOR_BGR2HSV)
    #redLower = np.array([0,100,100])
    #redUpper = np.array([5,255,255])
    redLower = np.array([-10,200,110])
    redUpper = np.array([10,240,240])
    mask = cv2.inRange(hsv, redLower, redUpper)
    redLower = np.array([170,200,130])
    redUpper = np.array([190,230,215])
    mask1 = cv2.inRange(hsv,redLower,redUpper)
    mask = cv2.addWeighted(mask,1.0,mask1,1,0,0)
    mask = cv2.dilate(mask, None, iterations=2)
    mask = cv2.erode(mask, None, iterations=2)

    cnts = cv2.findContours(mask.copy(), cv2.RETR_EXTERNAL,
		cv2.CHAIN_APPROX_SIMPLE)[-2]
    max_x = 0
    max_y = 0
    dirX = "s"
    dirY = "s"

    try:
        cnts = cv2.findContours(mask.copy(),cv2.RETR_EXTERNAL,cv2.CHAIN_APPROX_SIMPLE)[-2]
        if len(cnts) > 0:
            #tts.say("Found the ball!")
            c = max(cnts,key=cv2.contourArea)
            ((x,y),radius) = cv2.minEnclosingCircle(c)
            M=cv2.moments(c)
            if(all(value == 0 for value in M.values())):
                asdf=0
            else:
                #print(x,y,radius)

                center = (int(M["m10"] / M["m00"]), int(M["m01"] / M["m00"]))
                if radius > 5:

                    cv2.circle(frame, (int(x), int(y)), int(radius),(0, 255, 255), 2)
                    circles= x,y,radius
                    circles = np.uint16(np.around(circles))
                    max_x = circles[0]
                    max_y = circles[1]
                    max_r = circles[2]

                    diameter = radius*2
                    actual_diameter = 65
                    focal_length = 300
                    calculated_cam_dist = actual_diameter*focal_length/diameter
                    theta = motion.getAngles("HeadPitch", True)
                    calculated_floor_dist = calculated_cam_dist*np.cos(theta)
                    global distance
                    distance = calculated_floor_dist

        dX = width/2 - circles[0]

        dY = height/2 - circles[1]


        (dirX,dirY) = ("s","s")

        if np.abs(dX) > 30:
            dirX = "l" if np.sign(dX) == 1 else "r"

    # ensure there is significant movement in the
    # y-direction
        if np.abs(dY) > 30:
            dirY = "u" if np.sign(dY) == 1 else "d"

    # handle when both directions are non-empty
        if dirX != "" and dirY != "":
            direction = "{}-{}".format(dirY, dirX)
        else:
            direction = dirX if dirX != "" else dirY

        cv2.putText(image, direction, (10, 30), cv2.FONT_HERSHEY_SIMPLEX,0.65, (0, 0, 255), 3)
        cv2.putText(image, "dx: {}, dy: {}".format(dX, dY),(10, image.shape[0] - 10), cv2.FONT_HERSHEY_SIMPLEX,0.35, (0, 0, 255), 1)


    except:
        #tts.say("I lost the ball!")
        dirX = "0"
        dirY = "0"

    CM = [dirX,dirY]

    return CM

def main():

    parser=argparse.ArgumentParser(description="""Mydescription""")
    parser.add_argument('-mEnabled', action='store_true', default=False)
    args = parser.parse_args()

    motionBool = args.mEnabled

    if motionBool:
        motion.setStiffnesses("Body", 1.0)

    postureProxy = ALProxy("ALRobotPosture", ip_addr, port_num)

    if motionBool:
        postureProxy.goToPosture("StandInit", 0.2)

    motion.setAngles("HeadPitch", 0.3, 0.1)
    tts.say("I'm starting to goal")

    feed(motionBool)

if __name__ == "__main__":
    main()
