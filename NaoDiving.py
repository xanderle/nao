# -*- encoding: UTF-8 -*-

''' Whole Body Motion: Head orientation control '''

import sys
import time
import math
from naoqi import ALProxy

NAO_IP = "127.0.0.1"
NAO_PORT = 62207


# class movementModule(ALModule):
#     """ A simple module able to react
#     to facedetection events
#
#     """
#     def __init__(self, name):
#         ALModule.__init__(self, name)
#         # No need for IP and port here because
#         # we have our Python broker connected to NAOqi broker
#
#         # Create a proxy to ALTextToSpeech for later use
#         self.tts = ALProxy("ALTextToSpeech")
#
#         # Subscribe to the FaceDetected event:
#         global memory
#         memory = ALProxy("ALMemory")
#         memory.subscribeToEvent("FaceDetected",
#             "HumanGreeter",
#             "diveLeft")
#
#

def StiffnessOn(proxy):
    # We use the "Body" name to signify the collection of all joints
    pNames = "Body"
    pStiffnessLists = 1.0
    pTimeLists = 1.0
    proxy.stiffnessInterpolation(pNames, pStiffnessLists, pTimeLists)


def main(robotIP, robotPort, direction):
    ''' Example of a whole body head orientation control
        Warning: Needs a PoseInit before executing
                 Whole body balancer must be inactivated at the end of the script
    '''
    # Init proxies.
    try:
        #motionProxy = ALProxy("ALMotion", robotIP, robotPort)
        motProxy = ALProxy('ALMotion', robotIP, robotPort)
    except Exception, e:
        print "Could not create proxy to ALMotion"
        print "Error was: ", e

    try:
        posProxy = ALProxy("ALRobotPosture", robotIP, robotPort)
    except Exception, e:
        print "Could not create proxy to ALRobotPosture"
        print "Error was: ", e

    # Set NAO in Stiffness On
    StiffnessOn(motProxy)

    # Send NAO to Pose Init
    posProxy.goToPosture("StandInit", 0.5)

    names = list()
    angles = list()
    times = list()

    if (direction=="left"):
        names.extend(['LHipRoll', 'LHipPitch', 'LKneePitch', 'LAnklePitch', 'LAnkleRoll'])
        angles.extend([[0.438], [-0.8], [2.11], [-1.186], [-0.09]])
        times.extend([[0.5], [0.5], [0.5], [0.5], [0.5]])

        names.append('LHipYawPitch')
        angles.append([0.1])
        times.append([0.5])

        names.extend(['RHipRoll', 'RHipPitch', 'RKneePitch', 'RAnklePitch', 'RAnkleRoll'])
        angles.extend([[0.0], [-0.3], [0.6871], [-0.3099], [0.54788]])
        times.extend([[0.5], [0.5], [0.5], [0.5], [0.5]])

        motProxy.post.angleInterpolation(names, angles, times, True)

        names = list()
        angles = list()

        names.extend(['LShoulderPitch', 'LShoulderRoll', 'LElbowYaw', 'LElbowRoll'])
        angles.extend([-1.1,             0.5,            0.1883,    -0.5016] )

        names.extend(['RShoulderPitch','RShoulderRoll', 'RElbowYaw', 'RElbowRoll'])
        angles.extend([1.5,             0.3403,          0.1226,       0.903])

        motProxy.angleInterpolationWithSpeed(names, angles, 1.0)

        motProxy.setStiffnesses('Body', 0)
        time.sleep(2)

        motProxy.setStiffnesses('RArm', 0.8)
        motProxy.setStiffnesses('LLeg', 0.6)
        motProxy.setStiffnesses('RLeg', 0.6)

        # move arm around body to shift balance
        motProxy.angleInterpolation(['RShoulderPitch','RShoulderRoll',   'RElbowYaw',     'RElbowRoll'],
                                  [[1.372, 2.085],  [-1.2916, -0.105], [-0.154, -0.130],[1.1888, 0.380]],
                                  [[0.4,   0.8],    [0.4,     0.8],    [0.4,    0.8],   [0.4,    0.8]], True)

        motProxy.setAngles('RLeg', [-0.5,0,0,0.6,0.2,-0.2], 0.2)
        motProxy.setAngles('LLeg', [-0.5,0,0,0.6,0.2, 0.2], 0.2)
        motProxy.setStiffnesses('RArm', 0)
    elif (direction=="right"):
        names.extend(['RHipRoll', 'RHipPitch', 'RKneePitch', 'RAnklePitch', 'RAnkleRoll'])
        angles.extend([[-0.438], [-0.8], [2.11], [-1.186], [0.09]])
        times.extend([[0.5], [0.5], [0.5], [0.5], [0.5]])
        
        names.append('LHipYawPitch')
        angles.append([0.1])
        times.append([0.5])
        
        names.extend(['LHipRoll', 'LHipPitch', 'LKneePitch', 'LAnklePitch', 'LAnkleRoll'])
        angles.extend([[0], [-0.3], [0.6871], [-0.3099], [-0.54788]])
        times.extend([[0.5], [0.5], [0.5], [0.5], [0.5]])

        motProxy.post.angleInterpolation(names, angles, times, True)
        
        names = list()
        angles = list()
        
        names.extend(['RShoulderPitch','RShoulderRoll', 'RElbowYaw', 'RElbowRoll'])
        angles.extend([-1.1, -0.5, 0.1883, 0.5016])
        
        names.extend(['LShoulderPitch', 'LShoulderRoll', 'LElbowYaw', 'LElbowRoll'])
        angles.extend([1.5, -0.3403, 0.1226, -0.903])

        motProxy.angleInterpolationWithSpeed(names, angles, 1.0)
        
        motProxy.setStiffnesses('Body', 0)

        time.sleep(2)

        motProxy.setStiffnesses('LArm', 0.8)
        motProxy.setStiffnesses('LLeg', 0.6)
        motProxy.setStiffnesses('RLeg', 0.6)
        motProxy.angleInterpolation(['LShoulderPitch','LShoulderRoll', 'LElbowYaw',      'LElbowRoll'], 
                                  [[1.372, 2.085],  [1.2916, 0.105], [-0.154, -0.130], [-1.1888, -0.380]], 
                                  [[0.4,   0.8],    [0.4,    0.8],   [0.4,    0.8],    [0.4,     0.8]], True)
        motProxy.setAngles('LLeg', [-0.5,0,0,0.6,0.2, 0.2], 0.2)    
        motProxy.setAngles('RLeg', [-0.5,0,0,0.6,0.2,-0.2], 0.2)
        motProxy.setStiffnesses('RArm', 0)

    # wait until nao has taken a pose or three seconds have passed
    now = time.time()
    while posProxy.getPosture() != 'Back' and \
          posProxy.getPosture() != 'Belly' and \
          time.time() - now < 3.0 :
        pass
        
    motProxy.setStiffnesses('Body',0.8)
    if posProxy.getPosture() == 'Back':
        backToStand()
        walkTo(0.1, 0.05, 1.5)

    elif posProxy.getPosture() == 'Belly':
        bellyToStand()
        walkTo(-0.1, -0.05, -1.5)
    else:
        print 'What the heck, I do not have a pose!'

if __name__ == "__main__":
    if len(sys.argv) < 2:
        print "Pass command line arguments dive direction, or IP, Port, and dive direction."
        print "For example, 'python NaoDiving.py left' or 'python NaoDiving.py 127.0.0.1 62207 right'."
    elif len(sys.argv) == 4:
        robotIp = sys.argv[1]
        robotPort = sys.argv[2]
        direction = sys.argv[3]
        main(robotIp, robotPort, direction)
    elif len(sys.argv) == 2:
        robotIp = NAO_IP
        robotPort = NAO_PORT
        direction = sys.argv[1]
        main(robotIp, robotPort, direction)