# # -*- encoding: UTF-8 -*-
#
# import sys
#
# from naoqi import ALProxy
#
# def main(robotIP):
#     try:
#         motion = ALProxy("ALMotion", robotIp, 50630)
#         postureProxy = ALProxy("ALRobotPosture", robotIP, 50630)
#     except Exception, e:
#         print "Could not create proxy to ALMotion"
#         print "Error was: ", e
#     postureProxy.goToPosture("StandInit", 1.0)
#     while(1):
#         motion.walkTo(0, 10, 0)
#         motion.walkTo(0, -10, 0)
#
# if __name__ == "__main__":
#     robotIp = "127.0.0.1"
#
#     if len(sys.argv) <= 1:
#         print "Usage python alrobotposture.py robotIP (optional default: 127.0.0.1)"
#     else:
#         robotIp = sys.argv[1]
#
#     main(robotIp)
import sys

from naoqi import ALProxy


def main(robotIP):

    try:
        postureProxy = ALProxy("ALRobotPosture", robotIP, 9559)
        motion = ALProxy("ALMotion", robotIP, 9559)
    except Exception, e:
        print "Could not create proxy to ALRobotPosture"
        print "Error was: ", e

    postureProxy.goToPosture("StandInit", 1)
    while(1):
        direction = raw_input('Input l or r')
        if(direction == 'l'):
            motion.moveToward(0, 0.7, 0)
        elif(direction == 'r'):
            motion.moveToward(0, -0.7, 0)
        elif(direction == 's'):
            motion.moveToward(0, 0, 0)

    print postureProxy.getPostureFamily()


if __name__ == "__main__":
    robotIp = "192.168.2.111"

    if len(sys.argv) <= 1:
        print "Usage python alrobotposture.py robotIP (optional default: 127.0.0.1)"
    else:
        robotIp = sys.argv[1]

    main(robotIp)
