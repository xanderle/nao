import sys
import numpy as np
import cv2
from copy import deepcopy
from naoqi import ALProxy

ip_addr = "192.168.0.100"
port_num = 9559

# get NAOqi module proxy
videoDevice = ALProxy('ALVideoDevice', ip_addr, port_num)
motion = ALProxy("ALMotion", ip_addr, port_num)
tts = ALProxy("ALTextToSpeech",ip_addr,port_num)



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
def feed():
    width = 320
    height = 240
    image = np.zeros((height, width, 3), np.uint8)
    while True:
        # get image
        result = videoDevice.getImageRemote(captureDevice);

        if result == None:
            print 'cannot capture.'
        elif result[6] == None:
            print 'no image data string.'
        else:
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
            # alignBody(image,frame)
            direction = drawCenterOfMass(image,frame)

            cv2.line(frame,(0,height/2),(width,height/2),(0,255,0),1)
            cv2.line(frame,(width/2,0),(width/2,height),(0,255,0),1)
            cv2.imshow("Big Brother", frame)
            # centre head on ball
            #centerHead(direction)
            # move left or right for ball
            alignWithBall(direction)

        # exit by [ESC]
        if cv2.waitKey(33) == 27:
            motion.moveToward(0,0,0)
            break
    videoDevice.unsubscribe(captureDevice)
def alignWithBall(directions):
    print directions
    angles = motion.getAngles("HeadYaw",True)
    #print angles
    if directions[0] == 'l':
        motion.moveToward(0, 0.8, 0)
    elif directions[0] == 'r':
        motion.moveToward(0, -0.8, 0)
    elif directions[0]=="s":
        motion.moveToward(0,0,0)
    else:
        motion.moveToward(0,0,0)

def alignBody(image,frame):

    gray_image = cv2.cvtColor(image,cv2.COLOR_BGR2GRAY)
    mask_white = cv2.inRange(gray_image,200,255)
    mask_image = cv2.bitwise_and(gray_image,mask_white)
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
            if np.abs(dy) > 20:

                if np.sign(dy) == 1:
                    motion.moveToward(0,0,0.1)
                    return 'l'
                else:
                    motion.moveToward(0,0,-0.1)
                    return 'r'
            else:
                motion.moveToward(0,0,0)
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

    if(direction[0] =='l'):
        motion.changeAngles('HeadYaw',0.1,0.1)
    elif(direction[0] =='r'):
        motion.changeAngles('HeadYaw',-0.1,0.1)
    elif(direction[0]=='s'):
        motion.changeAngles('HeadYaw',0.0,0.1)

def drawCenterOfMass(image,frame):
    height,width,channels = image.shape
    hsv = cv2.cvtColor(image, cv2.COLOR_BGR2HSV)
    redLower = np.array([0,100,100])
    redUpper = np.array([5,255,255])

    mask = cv2.inRange(hsv, redLower, redUpper)
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
                if radius > 10:

                    cv2.circle(frame, (int(x), int(y)), int(radius),(0, 255, 255), 2)
                    circles= x,y,radius
                    circles = np.uint16(np.around(circles))
                    max_x = circles[0]
                    max_y = circles[1]
                    max_r = circles[2]


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
        max_x = 0
        max_y = 0

    CM = [dirX,dirY]

    return CM

def main():

    motion.setStiffnesses("Body", 1.0)

    postureProxy = ALProxy("ALRobotPosture", ip_addr, port_num)

    postureProxy.goToPosture("StandInit", 0.2)

    motion.setAngles("HeadPitch",0.3,0.1)
    tts.say("Looking for the ball!")
    feed()

if __name__ == "__main__":
    main()
