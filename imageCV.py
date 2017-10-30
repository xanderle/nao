import sys
import numpy as np
import cv2

from naoqi import ALProxy

ip_addr = "169.254.232.44"
port_num = 9559

# get NAOqi module proxy
videoDevice = ALProxy('ALVideoDevice', ip_addr, port_num)

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
            drawCenterOfMass(image)
            cv2.line(image,(0,height/2),(width,height/2),(0,255,0),1)
            cv2.line(image,(width/2,0),(width/2,height),(0,255,0),1)
            cv2.imshow("Big Brother",image)
    	    #
        # exit by [ESC]
        if cv2.waitKey(33) == 27:
            break
    videoDevice.unsubscribe(captureDevice)

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

    try:
        cnts = cv2.findContours(mask.copy(),cv2.RETR_EXTERNAL,cv2.CHAIN_APPROX_SIMPLE)[-2]
        if len(cnts) > 0:
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

        print"Out of if"
        dX = width/2 - circles[0]
        print "dx", dX
        dY = height/2 - circles[1]
        print "dy" ,dY

        (dirX,dirY) = ("","")

        if np.abs(dX) > 20:
            dirX = "East" if np.sign(dX) == 1 else "West"

    # ensure there is significant movement in the
    # y-direction
        if np.abs(dY) > 20:
            dirY = "North" if np.sign(dY) == 1 else "South"

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

    CM = [max_y,max_x]
    return CM

def main():
    feed()

if __name__ == "__main__":
    main()
