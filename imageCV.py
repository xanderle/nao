import sys
import numpy as np
import cv2

from naoqi import ALProxy
from naoqi import ALModule
from naoqi import ALBroker


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


class FallDetectionModule(ALModule):
    """ A simple module able to react
    to facedetection events

    """
    def __init__(self, name):
        ALModule.__init__(self, name)
        # No need for IP and port here because
        # we have our Python broker connected to NAOqi broker

        # Create a proxy to ALTextToSpeech for later use
        self.tts = ALProxy("ALTextToSpeech")

        # Subscribe to the FaceDetected event:
        global memory
        memory = ALProxy("ALMemory")
        memory.subscribeToEvent("robotHasFallen",
            "FallDetection",
            "FallDetected")

    def FallDetected(self, *_args):
        """ This will be called each time a face is
        detected.

        """
        # Unsubscribe to the event when talking,
        # to avoid repetitions
        memory.unsubscribeToEvent("robotHasFallen",
            "FallDetection")

        self.tts.say("I have fallen")
        postureProxy.goToPosture("StandInit", 0.2)
        # Subscribe again to the event
        memory.subscribeToEvent("robotHasFallen",
            "FallDetection",
            "FallDetected")

def feed():

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
            direction = drawCenterOfMass(image)
            cv2.line(image,(0,height/2),(width,height/2),(0,255,0),1)
            cv2.line(image,(width/2,0),(width/2,height),(0,255,0),1)
            cv2.imshow("Big Brother",image)
            # centre head on ball
            centerHead(direction)
            # move left or right for ball
            alignWithBall(direction)

        # exit by [ESC]
        if cv2.waitKey(33) == 27:
            motion.moveToward(0, 0, 0)
            break
    videoDevice.unsubscribe(captureDevice)

def alignWithBall(directions):
    angles = motion.getAngles("HeadYaw",True)
    print angles
    if angles[0] > 0.087:
        motion.moveToward(0, 0.5, 0)
    elif angles[0] < -0.087:
        motion.moveToward(0, -0.5, 0)
    elif directions[0]=="s":
        motion.moveToward(0,0,0)
    else:
        motion.moveToward(0,0,0)
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

def drawCenterOfMass(image):
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

                    cv2.circle(image, (int(x), int(y)), int(radius),(0, 255, 255), 2)
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
    myBroker = ALBroker("myBroker","0.0.0.0",   0,ip_addr,port_num)


    motion.setStiffnesses("Body", 1.0)

    global FallDetection
    FallDetection = FallDetectionModule("FallDetection")


    postureProxy = ALProxy("ALRobotPosture", ip_addr, port_num)

    postureProxy.goToPosture("StandInit", 0.2)

    motion.setAngles("HeadPitch",0.3,0.1)
    tts.say("Looking for the ball!")
    feed()

if __name__ == "__main__":
    main()
