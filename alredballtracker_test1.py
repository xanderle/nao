# -*- encoding: UTF-8 -*-

"""
This example shows how to use ALTracker with red ball.
"""
# Adapted from <http://doc.aldebaran.com/2-1/naoqi/trackers/trackers-sample.html>

# And testing some of the methods from ALMotion and AlTracker
# such as .angleInterpolation() to change joint angle in neck to make nao look downward.
# .moveTo() to send command for nao to walk to specified (x,y) coordinate with specified angle.
# .getTargetPosition() to get coordintates relative to specified frame (e.g. ROBOT_FRAME).

# <http://doc.aldebaran.com/2-1/naoqi/motion/almotion-api.html#almotion-api>
# <http://doc.aldebaran.com/2-1/naoqi/trackers/altracker-api.html>

import math
import time
import argparse
from naoqi import ALProxy

def main(IP, PORT, ballSize):

    print "Connecting to", IP, "with port", PORT
    motion = ALProxy("ALMotion", IP, PORT)
    posture = ALProxy("ALRobotPosture", IP, PORT)
    tracker = ALProxy("ALTracker", IP, PORT)

    # First, wake up.
    motion.wakeUp()

    fractionMaxSpeed = 0.8
    # Go to posture stand
    posture.goToPosture("StandInit", fractionMaxSpeed)

    # Add target to track.
    targetName = "RedBall"
    diameterOfBall = ballSize
    tracker.registerTarget(targetName, diameterOfBall)

    # set mode
    mode = "Head"
    tracker.setMode(mode)

    #look down
    names = "HeadPitch" #Rotate head downward.
    angleLists = 0.52 #angle in rad + is downward, - is upward.
    times = 5.0 #time in seconds.
    isAbsolute = True
    motion.angleInterpolation(names, angleLists, times, isAbsolute)

    # Then, start tracker.
    tracker.track(targetName)

    print "ALTracker successfully started, now show a red ball to robot!"
    print "Use Ctrl+c to stop this script."

    try:
        while True:
            [target_x, target_y, target_z] = tracker.getTargetPosition(2) #Use AlTracker method .getTargetPosition to retrieve coordintates relative to ROBOT_FRAME.
            print target_x, target_y, target_z
            angleToTurn = math.atan2(target_y,target_x)
            print "angleToTurn = ", angleToTurn
            print "angleToTurn in deg= ", angleToTurn*180/math.pi
            motion.moveTo(0, 0, angleToTurn) #Rotate on the spot towards target (red ball).
            motion.moveTo(math.sqrt(target_x**2 + target_y**2), 0, 0) #Walk straight to target.
            break; #Only run this once for now.
            time.sleep(1)
    except KeyboardInterrupt:
        print
        print "Interrupted by user"
        print "Stopping..."

    # Stop tracker, go to posture Sit.
    tracker.stopTracker()
    tracker.unregisterAllTargets()
    motion.rest()

    print "ALTracker stopped."


if __name__ == "__main__" :

    parser = argparse.ArgumentParser()
    parser.add_argument("--ip", type=str, default="192.168.2.121",
                        help="Robot ip address.")
    parser.add_argument("--port", type=int, default=9559,
                        help="Robot port number.")
    parser.add_argument("--ballsize", type=float, default=0.06,
                        help="Diameter of ball.")

    args = parser.parse_args()

    main(args.ip, args.port, args.ballsize)
