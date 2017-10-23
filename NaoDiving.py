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
    
# Stand up from the back
def backToStand(motProxy, posProxy):
    # lie down on back, move arms towards pushing position and legs upwards
    motProxy.setAngles(['HeadPitch', 'HeadYaw'], [-0.4, 0.0], 0.4)
    motProxy.post.angleInterpolation(['LShoulderPitch', 'LShoulderRoll' ,'LElbowRoll', 'LElbowYaw'],
                              [[-0.1, 0.8],       [1, 0.5] ,      [ -1.5],        [1.9]       ],\
                              [[0.4, 0.8],        [0.5, 0.8],     [0.5],          [0.5]],  True)                
    motProxy.post.angleInterpolation(['RShoulderPitch', 'RShoulderRoll', 'RElbowRoll', 'RElbowYaw'],
                              [[0, 0.8],          [-1.0, -0.5],   [1.5],          [-1.9]],
                              [[0.5, 0.8],        [0.5, 0.8],     [0.5],          [0.5]],  True)
                            
    motProxy.setAngles(['LHipYawPitch', 'RKneePitch', 'LKneePitch', 'RHipRoll', 'LHipRoll', 'RAnkleRoll', 'LAnkleRoll'],
                [0             ,  0           , 0          ,  0        ,  0        ,  0          ,  0          ],  0.3)
    motProxy.setAngles( ['LHipPitch', 'LAnklePitch', 'RHipPitch', 'RAnklePitch'],
                 [-1.5       , 0.8          , -1.5,       0.8], 0.3 )
    time.sleep(1)

    # move legs down, arms down to push
    motProxy.setAngles(['LShoulderPitch','RShoulderPitch','RHipPitch', 'LHipPitch'],
                [2               , 2              , -0.7        ,  -0.7        ],  0.9)
    time.sleep(0.1)
    # reset legs
    motProxy.setAngles(['RHipPitch', 'LHipPitch'], [ -1.5, -1.5 ],  0.3 )
    time.sleep(0.2)
    # push up with arms
    motProxy.setAngles(['RShoulderRoll', 'LShoulderRoll'], [-0.25, 0.25], 0.5 )
    motProxy.setAngles(['LElbowRoll', 'RElbowRoll'], [0,0], 0.5)
    
    time.sleep(0.4)
    
    # twist legs around to sit with legs wide
    t = 0.4
    names = list()
    angles = list()
    times = list()
        
    names.extend(['RShoulderPitch', 'RShoulderRoll', 'RElbowYaw', 'RElbowRoll'])
    angles.extend([[2],           [-0.3],            [0.7] ,     [0.06]])
    times.extend([[t],              [t],              [t],         [t]])
    
    names.extend(['LShoulderPitch', 'LShoulderRoll', 'LElbowYaw', 'LElbowRoll'])
    angles.extend([[2],           [0.3],           [-0.7] ,     [-0.05]])
    times.extend([[t],              [t],             [t],         [t]])
    
    names.extend(['LHipYawPitch', 'RHipRoll', 'RHipPitch', 'RKneePitch', 'RAnklePitch', 'RAnkleRoll'])
    angles.extend([[-0.7],       [-0.23],    [-1.57],      [0.8],       [0.85],        [0.06]])
    times.extend([[t],            [t],        [t],         [t],          [t],           [t]])
    
    names.extend(['LHipRoll', 'LHipPitch', 'LKneePitch', 'LAnklePitch', 'LAnkleRoll'])
    angles.extend([[0.23],    [-1.57],      [0.8],       [0.85],        [-0.06]])
    times.extend([[t],        [t],         [t],          [t],           [t]])    
    motProxy.angleInterpolation(names, angles, times, True)
    
    # move one arm backwards, one arm upwards, move legs towards body
    motProxy.setAngles(['HeadPitch', 'HeadYaw'], [0.5, 0.0], 0.4)
    t = 0.4
    names = list()
    angles = list()
    times = list()
        
    names.extend(['RShoulderPitch', 'RShoulderRoll', 'RElbowYaw', 'RElbowRoll'])
    angles.extend([[2.085], [-0.3], [0.6764], [0.055]])
    times.extend([[t],              [t],              [t],         [t]])
    
    names.extend(['LShoulderPitch', 'LShoulderRoll', 'LElbowYaw', 'LElbowRoll'])
    angles.extend([[0.56],          [0.52],          [-0.33],     [-.55]])
    times.extend([[t],              [t],             [t],         [t]])
    
    names.extend(['LHipYawPitch', 'RHipRoll', 'RHipPitch', 'RKneePitch', 'RAnklePitch', 'RAnkleRoll'])
    angles.extend([[-0.89],       [-0.57],   [-1.31],      [0.73],       [0.93],        [0.07]])
    times.extend([[t],            [t],        [t],         [t],          [t],           [t]])
    
    names.extend(['LHipRoll', 'LHipPitch', 'LKneePitch', 'LAnklePitch', 'LAnkleRoll'])
    angles.extend([[0.54],      [-1.05],    [2.11],       [-0.13],       [-0.25]])
    times.extend([[t],        [t],         [t],          [t],           [t]])
    motProxy.angleInterpolation(names, angles, times, True)
    
    # move legs further towards body
    t = 0.6
    names = list()
    angles = list()
    times = list()
    
    names.extend(['LHipYawPitch', 'RHipRoll', 'RHipPitch', 'RKneePitch', 'RAnklePitch', 'RAnkleRoll'])
    angles.extend([[-1.07],      [-0.656],   [-1.67],      [1.63 ],       [0.32],       [-0.004]])
    times.extend([[t],            [t],        [t],         [t],          [t],           [t]])
    
    names.extend(['LHipRoll', 'LHipPitch', 'LKneePitch', 'LAnklePitch', 'LAnkleRoll'])
    angles.extend([[-0.01], [-0.01],     [2.11254]    , [-1] , [0.10128598]])
    times.extend([[t],        [t],         [t],          [t],           [t]])
    motProxy.angleInterpolation(names, angles, times, True)

    # Lift arm from ground, move right leg towards body
    t = 0.3
    names = list()
    angles = list()
    times = list()
        
    names.extend(['RShoulderPitch', 'RShoulderRoll', 'RElbowYaw', 'RElbowRoll'])
    angles.extend([[1.86205],      [-0.5913],       [0.61815],   [0.0598679]])
    times.extend([[t],              [t],              [t],         [t]])
    
    names.extend(['LShoulderPitch', 'LShoulderRoll', 'LElbowYaw', 'LElbowRoll'])
    angles.extend([[0.98],          [0.531],         [-0.03],     [-0.57]])
    times.extend([[t],              [t],             [t],         [t]])
    
    names.extend(['RHipRoll', 'RHipPitch', 'RKneePitch', 'RAnklePitch', 'RAnkleRoll'])
    angles.extend([[-0.73],    [-1.47],     [2],         [-0.13],      [0.15]])
    times.extend([[t],            [t],        [t],         [t],          [t]])
    
    names.extend(['LAnklePitch'])
    angles.extend([[-1.18]])
    times.extend([[t]])
    
    motProxy.angleInterpolation(names, angles, times, True)
    
    # lift right leg further towards left
    t = 0.4
    names = list()
    angles = list()
    times = list()
    
    names.extend(['LHipYawPitch', 'RHipRoll', 'RHipPitch', 'RKneePitch', 'RAnklePitch', 'RAnkleRoll'])
    angles.extend([[-0.5],      [-0.2],   [-0.55],      [2.11 ],       [-1.18],       [0.07]])
    times.extend([[t],            [t],        [t],         [t],          [t],           [t]])
    
    names.extend(['LHipRoll', 'LHipPitch', 'LKneePitch', 'LAnklePitch', 'LAnkleRoll'])
    angles.extend([[0.2],    [-0.55],     [2.11],       [-1.18] ,  [-0.07 ]])
    times.extend([[t],        [t],         [t],          [t],           [t]])
    motProxy.angleInterpolation(names, angles, times, True)
    
    # move legs closer to eachother (stance)
    t = 0.2
    names = list()
    angles = list()
    times = list()
    
    names.extend(['LHipYawPitch', 'RHipRoll', 'RHipPitch', 'RKneePitch', 'RAnklePitch', 'RAnkleRoll'])
    angles.extend([[0],           [0],        [-0.9],      [2.11 ],       [-1.18],       [0.0]])
    times.extend([[t],            [t],        [t],         [t],          [t],           [t]])
    
    names.extend(['LHipRoll', 'LHipPitch', 'LKneePitch', 'LAnklePitch', 'LAnkleRoll'])
    angles.extend([[0],        [-0.9],      [2.11 ],       [-1.18],       [0.0]])
    times.extend([[t],        [t],         [t],          [t],           [t]])
    motProxy.angleInterpolation(names, angles, times, True)        
    
    posProxy.goToPosture("StandInit", 0.5)
    
# Stand up from belly
def bellyToStand(motProxy, posProxy):
    names = list()
    times = list()
    angles = list()
    
    names.append('HeadYaw')
    times.append([0.5, 1.0, 1.7, 2.3, 2.9, 3.7, 4.4, 5.2, 6.5])
    angles.append([ [ 0.17453, [ 3, -0.33333, 0.00000], [ 3, 0.33333, 0.00000]],
                    [ -0.22689, [ 3, -0.33333, 0.00000], [ 3, 0.46667, 0.00000]],
                    [ 0.28623, [ 3, -0.46667, -0.01333], [ 3, 0.36667, 0.01047]],
                    [ 0.29671, [ 3, -0.36667, 0.00000], [ 3, 0.43333, 0.00000]],
                    [ -0.49567, [ 3, -0.43333, 0.00000], [ 3, 0.23333, 0.00000]],
                    [ -0.29671, [ 3, -0.23333, -0.07104], [ 3, 0.36667, 0.11164]],
                    [ 0.05236, [ 3, -0.36667, 0.00000], [ 3, 0.43333, 0.00000]],
                    [ -0.39095, [ 3, -0.43333, 0.00000], [ 3, 0.36667, 0.00000]],
                    [ 0.0, [ 3, -0.36667, 0.00000], [ 3, 0.00000, 0.00000]]])

    names.append('HeadPitch')
    times.append([0.5, 1.0, 1.7, 2.3, 2.9, 3.7, 4.4, 5.2, 6.5])
    angles.append([ [ -0.57683, [ 3, -0.33333, 0.00000], [ 3, 0.33333, 0.00000]],
                    [ -0.54768, [ 3, -0.33333, -0.02915], [ 3, 0.46667, 0.04081]],
                    [ 0.10734, [ 3, -0.46667, -0.19834], [ 3, 0.36667, 0.15584]],
                    [ 0.51487, [ 3, -0.36667, 0.00000], [ 3, 0.43333, 0.00000]],
                    [ 0.38048, [ 3, -0.43333, 0.01726], [ 3, 0.23333, -0.00930]],
                    [ 0.37119, [ 3, -0.23333, 0.00930], [ 3, 0.36667, -0.01461]],
                    [ -0.10472, [ 3, -0.36667, 0.13827], [ 3, 0.43333, -0.16341]],
                    [ -0.53387, [ 3, -0.43333, 0.00000], [ 3, 0.36667, 0.00000]],
                    [ -0.5, [ 3, -0.36667, 0.00000], [ 3, 0.00000, 0.00000]]])

    names.append('LShoulderPitch')
    times.append([0.2, 0.5, 0.8, 1.7, 2.3, 2.9, 3.7, 4.4, 5.2, 6.5])
    angles.append([ [2, [ 3, -0.33333, 0.00000], [ 3, 0.33333, 0.00000]],
                    [ -0.02757, [ 3, -0.33333, 0.00000], [ 3, 0.33333, 0.00000]],
                    [ -1.51146, [ 3, -0.33333, 0.00000], [ 3, 0.46667, 0.00000]],
                    [ -1.25025, [ 3, -0.46667, -0.26120], [ 3, 0.36667, 0.20523]],
                    [ 0.07206, [ 3, -0.36667, -0.38566], [ 3, 0.43333, 0.45578]],
                    [ 1.27409, [ 3, -0.43333, 0.00000], [ 3, 0.23333, 0.00000]],
                    [ 0.75573, [ 3, -0.23333, 0.00333], [ 3, 0.36667, -0.00524]],
                    [ 0.75049, [ 3, -0.36667, 0.00000], [ 3, 0.43333, 0.00000]],
                    [ 1.29154, [ 3, -0.43333, -0.15226], [ 3, 0.36667, 0.12884]],
                    [ 1.2, [ 3, -0.36667, 0.00000], [ 3, 0.00000, 0.00000]]])

    names.append('LShoulderRoll')
    times.append([0.3, 1.0, 1.7, 2.3, 2.9, 3.7, 4.4, 5.2, 6.5])
    angles.append([ [ 1.55390, [ 3, -0.33333, 0.00000], [ 3, 0.33333, 0.00000]],
                    [ 0.01683, [ 3, -0.33333, 0.00000], [ 3, 0.46667, 0.00000]],
                    [ 0.07666, [ 3, -0.46667, 0.00000], [ 3, 0.36667, 0.00000]],
                    [ 0.07052, [ 3, -0.36667, 0.00000], [ 3, 0.43333, 0.00000]],
                    [ 0.15643, [ 3, -0.43333, -0.08590], [ 3, 0.23333, 0.04626]],
                    [ 0.93899, [ 3, -0.23333, 0.00000], [ 3, 0.36667, 0.00000]],
                    [ 0.67719, [ 3, -0.36667, 0.00000], [ 3, 0.43333, 0.00000]],
                    [ 0.84648, [ 3, -0.43333, 0.00000], [ 3, 0.36667, 0.00000]],
                    [ 0.2, [ 3, -0.36667, 0.00000], [ 3, 0.00000, 0.00000]]])

    names.append('LElbowYaw')
    times.append([0.5, 1.0, 1.7, 2.3, 2.9, 3.7, 4.4, 5.2, 6.5])
    angles.append([ [ -2.07694, [ 3, -0.33333, 0.00000], [ 3, 0.33333, 0.00000]],
                    [ -1.58006, [ 3, -0.33333, 0.00000], [ 3, 0.46667, 0.00000]],
                    [ -1.60461, [ 3, -0.46667, 0.02454], [ 3, 0.36667, -0.01928]],
                    [ -1.78715, [ 3, -0.36667, 0.00000], [ 3, 0.43333, 0.00000]],
                    [ -1.32695, [ 3, -0.43333, -0.11683], [ 3, 0.23333, 0.06291]],
                    [ -1.24791, [ 3, -0.23333, -0.04593], [ 3, 0.36667, 0.07218]],
                    [ -0.97260, [ 3, -0.36667, -0.01072], [ 3, 0.43333, 0.01267]],
                    [ -0.95993, [ 3, -0.43333, 0.00000], [ 3, 0.36667, 0.00000]],
                    [ 0, [ 3, -0.36667, 0.00000], [ 3, 0.00000, 0.00000]]])

    names.append('LElbowRoll')
    times.append([0.5, 1.0, 1.7, 2.3, 2.9, 3.7, 4.4, 5.2, 6.5])
    angles.append([ [ -0.00873, [ 3, -0.33333, 0.00000], [ 3, 0.33333, 0.00000]],
                    [ -0.35278, [ 3, -0.33333, 0.08741], [ 3, 0.46667, -0.12238]],
                    [ -0.63810, [ 3, -0.46667, 0.09306], [ 3, 0.36667, -0.07312]],
                    [ -0.85133, [ 3, -0.36667, 0.13944], [ 3, 0.43333, -0.16480]],
                    [ -1.55083, [ 3, -0.43333, 0.00000], [ 3, 0.23333, 0.00000]],
                    [ -0.73304, [ 3, -0.23333, 0.00000], [ 3, 0.36667, 0.00000]],
                    [ -0.73653, [ 3, -0.36667, 0.00349], [ 3, 0.43333, -0.00413]],
                    [ -1.15506, [ 3, -0.43333, 0.00000], [ 3, 0.36667, 0.00000]],
                    [ 0, [ 3, -0.36667, 0.00000], [ 3, 0.00000, 0.00000]]])

    names.append('RShoulderPitch')
    times.append([0.2, 0.5, 1.0, 1.7, 2.3, 2.9, 3.7, 4.4, 5.2, 6.5])
    angles.append([ [2, [ 3, -0.33333, 0.00000], [ 3, 0.33333, 0.00000]],
                    [ -0.02757, [ 3, -0.33333, 0.00000 ], [ 3, 0.33333, 0.00000]],
                    [ -1.51146, [ 3, -0.33333, 0.00000 ], [ 3, 0.46667, 0.00000]],
                    [ -1.22256, [ 3, -0.46667, -0.23805], [ 3, 0.36667, 0.18704]],
                    [ -0.23619, [ 3, -0.36667, -0.22007], [ 3, 0.43333, 0.26008]],
                    [ 0.21787, [ 3, -0.43333, -0.14857 ], [ 3, 0.23333, 0.08000]],
                    [ 0.44950, [ 3, -0.23333, -0.09028 ], [ 3, 0.36667, 0.14187]],
                    [ 0.91431, [ 3, -0.36667, -0.03894 ], [ 3, 0.43333, 0.04602]],
                    [ 0.96033, [ 3, -0.43333, -0.04602 ], [ 3, 0.36667, 0.03894]],
                    [ 1.2, [ 3, -0.36667, 0.00000], [ 3, 0.00000, 0.00000]]])

    names.append('RShoulderRoll')
    times.append([0.3, 1.0, 1.7, 2.3, 2.9, 3.7, 4.4, 5.2, 6.5])
    angles.append([ [ -1.53558, [ 3, -0.33333, 0.00000], [ 3, 0.33333, 0.00000]],
                    [ -0.19199, [ 3, -0.33333, -0.07793], [ 3, 0.46667, 0.10911]],
                    [ -0.08288, [ 3, -0.46667, 0.00000], [ 3, 0.36667, 0.00000]],
                    [ -0.08288, [ 3, -0.36667, 0.00000], [ 3, 0.43333, 0.00000]],
                    [ -0.22707, [ 3, -0.43333, 0.00000], [ 3, 0.23333, 0.00000]],
                    [ -0.18259, [ 3, -0.23333, -0.02831], [ 3, 0.36667, 0.04448]],
                    [ -0.00870, [ 3, -0.36667, 0.00000], [ 3, 0.43333, 0.00000]],
                    [ -0.13197, [ 3, -0.43333, 0.01994], [ 3, 0.36667, -0.01687]],
                    [ -0.2, [ 3, -0.36667, 0.00000], [ 3, 0.00000, 0.00000]]])

    names.append('RElbowYaw')
    times.append([0.5, 1.0, 1.7, 2.3, 2.9, 3.7, 4.4, 5.2, 6.5])
    angles.append([ [ 2.07694, [ 3, -0.33333, 0.00000 ], [ 3, 0.33333, 0.00000]],
                    [ 1.56157, [ 3, -0.33333, 0.00000 ], [ 3, 0.46667, 0.00000]],
                    [ 1.61373, [ 3, -0.46667, -0.02319], [ 3, 0.36667, 0.01822]],
                    [ 1.68582, [ 3, -0.36667, -0.05296], [ 3, 0.43333, 0.06259]],
                    [ 1.96041, [ 3, -0.43333, 0.00000 ], [ 3, 0.23333, 0.00000]],
                    [ 1.95121, [ 3, -0.23333, 0.00920 ], [ 3, 0.36667, -0.01445]],
                    [ 0.66571, [ 3, -0.36667, 0.22845 ], [ 3, 0.43333, -0.26998]],
                    [ 0.39573, [ 3, -0.43333, 0.00000 ], [ 3, 0.36667, 0.00000]],
                    [ 0, [ 3, -0.36667, 0.00000], [ 3, 0.00000, 0.00000]]])

    names.append('RElbowRoll')
    times.append([0.5, 1.0, 1.7, 2.3, 2.9, 3.7, 4.4, 5.2, 6.5])
    angles.append([ [ 0.10472, [ 3, -0.33333, 0.00000], [ 3, 0.33333, 0.00000]],
                    [ 0.38201, [ 3, -0.33333, -0.07367], [ 3, 0.46667, 0.10313]],
                    [ 0.63512, [ 3, -0.46667, -0.21934], [ 3, 0.36667, 0.17234]],
                    [ 1.55705, [ 3, -0.36667, 0.00000], [ 3, 0.43333, 0.00000]],
                    [ 0.00870, [ 3, -0.43333, 0.00000], [ 3, 0.23333, 0.00000]],
                    [ 0.00870, [ 3, -0.23333, 0.00000], [ 3, 0.36667, 0.00000]],
                    [ 0.42343, [ 3, -0.36667, -0.09786], [ 3, 0.43333, 0.11566]],
                    [ 0.64926, [ 3, -0.43333, 0.00000], [ 3, 0.36667, 0.00000]],
                    [ 0.0, [ 3, -0.36667, 0.00000], [ 3, 0.00000, 0.00000]]])

    names.append('LHipYawPitch')
    times.append([0.5, 1.0, 1.7, 2.3, 2.9, 3.7, 4.4, 5.2, 6.5])
    angles.append([ [ -0.03371, [ 3, -0.33333, 0.00000], [ 3, 0.33333, 0.00000]],
                    [ 0.03491, [ 3, -0.33333, 0.00000], [ 3, 0.46667, 0.00000]],
                    [ -0.43561, [ 3, -0.46667, 0.15197], [ 3, 0.36667, -0.11941]],
                    [ -0.77923, [ 3, -0.36667, 0.09257], [ 3, 0.43333, -0.10940]],
                    [ -1.04154, [ 3, -0.43333, 0.07932], [ 3, 0.23333, -0.04271]],
                    [ -1.530, [ 3, -0.23333, 0.00000], [ 3, 0.36667, 0.00000]],
                    [ -1, [ 3, -0.36667, 0.00000], [ 3, 0.43333, 0.00000]],
                    [ -0.56754, [ 3, -0.43333, -0.16414], [ 3, 0.36667, 0.13889]],
                    [ 0.0, [ 3, -0.36667, 0.00000], [ 3, 0.00000, 0.00000]]])

    names.append('LHipRoll')
    times.append([0.5, 1.0, 1.7, 2.3, 2.9, 3.7, 4.4, 5.2, 6.5])
    angles.append([ [ 0.06294, [ 3, -0.33333, 0.00000], [ 3, 0.33333, 0.00000]],
                    [ 0.00004, [ 3, -0.33333, 0.00000], [ 3, 0.46667, 0.00000]],
                    [ 0.00158, [ 3, -0.46667, 0.00000], [ 3, 0.36667, 0.00000]],
                    [ -0.37732, [ 3, -0.36667, 0.00000], [ 3, 0.43333, 0.00000]],
                    [ -0.29755, [ 3, -0.43333, 0.00000], [ 3, 0.23333, 0.00000]],
                    [ -0.29755, [ 3, -0.23333, 0.00000], [ 3, 0.36667, 0.00000]],
                    [ 0.19486, [ 3, -0.36667, 0.00000], [ 3, 0.43333, 0.00000]],
                    [ 0.12736, [ 3, -0.43333, 0.00000], [ 3, 0.36667, 0.00000]],
                    [ 0.0, [ 3, -0.36667, 0.00000], [ 3, 0.00000, 0.00000]]])

    names.append('LHipPitch')
    times.append([0.5, 1.0, 1.7, 2.3, 2.9, 3.7, 4.4, 5.2, 6.5])
    angles.append([ [ 0.06140, [ 3, -0.33333, 0.00000], [ 3, 0.33333, 0.00000]],
                    [ 0.00004, [ 3, -0.33333, 0.06136], [ 3, 0.46667, -0.08590]],
                    [ -1.56924, [ 3, -0.46667, 0.00000], [ 3, 0.36667, 0.00000]],
                    [ -1.28085, [ 3, -0.36667, -0.08132], [ 3, 0.43333, 0.09611]],
                    [ -1.03694, [ 3, -0.43333, 0.00000], [ 3, 0.23333, 0.00000]],
                    [ -1.15966, [ 3, -0.23333, 0.01464], [ 3, 0.36667, -0.02301]],
                    [ -1.18267, [ 3, -0.36667, 0.01687], [ 3, 0.43333, -0.01994]],
                    [ -1.27011, [ 3, -0.43333, 0.00000], [ 3, 0.36667, 0.00000]],
                    [ -0.4, [ 3, -0.36667, 0.00000], [ 3, 0.00000, 0.00000]]])

    names.append('LKneePitch')
    times.append([0.5, 1.0, 1.7, 2.3, 2.9, 3.7, 4.4, 5.2, 6.5])
    angles.append([ [ 0.12043, [ 3, -0.33333, 0.00000], [ 3, 0.33333, 0.00000]],
                    [ 1.98968, [ 3, -0.33333, -0.08775], [ 3, 0.46667, 0.12285]],
                    [ 2.11253, [ 3, -0.46667, 0.00000], [ 3, 0.36667, 0.00000]],
                    [ 0.28221, [ 3, -0.36667, 0.00000], [ 3, 0.43333, 0.00000]],
                    [ 0.40493, [ 3, -0.43333, 0.00000], [ 3, 0.23333, 0.00000]],
                    [ 0.35738, [ 3, -0.23333, 0.00000], [ 3, 0.36667, 0.00000]],
                    [ 0.71940, [ 3, -0.36667, -0.25311], [ 3, 0.43333, 0.29913]],
                    [ 2.01409, [ 3, -0.43333, 0.00000], [ 3, 0.36667, 0.00000]],
                    [ 0.95, [ 3, -0.36667, 0.00000], [ 3, 0.00000, 0.00000]]])

    names.append('LAnklePitch')
    times.append([0.5, 1.0, 1.7, 2.3, 2.9, 3.7, 4.4, 5.2, 6.5])
    angles.append([ [ 0.92189, [ 3, -0.33333, 0.00000], [ 3, 0.33333, 0.00000]],
                    [ -1.02974, [ 3, -0.33333, 0.08628], [ 3, 0.46667, -0.12080]],
                    [ -1.15054, [ 3, -0.46667, 0.00000], [ 3, 0.36667, 0.00000]],
                    [ 0.21625, [ 3, -0.36667, -0.28428], [ 3, 0.43333, 0.33597]],
                    [ 0.71020, [ 3, -0.43333, -0.15307], [ 3, 0.23333, 0.08242]],
                    [ 0.92275, [ 3, -0.23333, 0.00000], [ 3, 0.36667, 0.00000]],
                    [ 0.82525, [ 3, -0.36667, 0.09750], [ 3, 0.43333, -0.11522]],
                    [ -0.50166, [ 3, -0.43333, 0.00000], [ 3, 0.36667, 0.00000]],
                    [ -0.55, [ 3, -0.36667, 0.00000], [ 3, 0.00000, 0.00000]]])

    names.append('LAnkleRoll')
    times.append([0.5, 1.0, 1.7, 2.3, 2.9, 3.7, 4.4, 5.2, 6.5])
    angles.append([ [ -0.00149, [ 3, -0.33333, 0.00000], [ 3, 0.33333, 0.00000]],
                    [ 0.00004,  [ 3, -0.33333, 0.00000], [ 3, 0.46667, 0.00000]],
                    [ -0.00149, [ 3, -0.46667, 0.00153], [ 3, 0.36667, -0.00121]],
                    [ -0.45249, [ 3, -0.36667, 0.00000], [ 3, 0.43333, 0.00000]],
                    [ -0.30062, [ 3, -0.43333, -0.07246], [ 3, 0.23333, 0.03901]],
                    [ -0.11808, [ 3, -0.23333, -0.03361], [ 3, 0.36667, 0.05281]],
                    [ -0.04138, [ 3, -0.36667, 0.00000], [ 3, 0.43333, 0.00000]],
                    [ -0.12114, [ 3, -0.43333, 0.01632], [ 3, 0.36667, -0.01381]],
                    [ 0.0, [ 3, -0.36667, 0.00000], [ 3, 0.00000, 0.00000]]])

    names.append('RHipRoll')
    times.append([0.5, 1.0, 1.7, 2.3, 2.9, 3.7, 4.4, 5.2, 6.5])
    angles.append([ [ 0.03142, [ 3, -0.33333, 0.00000], [ 3, 0.33333, 0.00000]],
                    [ 0.00004, [ 3, -0.33333, 0.00000], [ 3, 0.46667, 0.00000]],
                    [ 0.00158, [ 3, -0.46667, -0.00153], [ 3, 0.36667, 0.00121]],
                    [ 0.31144, [ 3, -0.36667, 0.00000], [ 3, 0.43333, 0.00000]],
                    [ 0.25469, [ 3, -0.43333, 0.00000], [ 3, 0.23333, 0.00000]],
                    [ 0.32065, [ 3, -0.23333, 0.00000], [ 3, 0.36667, 0.00000]],
                    [ 0.22707, [ 3, -0.36667, 0.06047], [ 3, 0.43333, -0.07146]],
                    [ -0.07512, [ 3, -0.43333, 0.00000], [ 3, 0.36667, 0.00000]],
                    [ 0, [ 3, -0.36667, 0.00000], [ 3, 0.00000, 0.00000]]])

    names.append('RHipPitch')
    times.append([0.5, 1.0, 1.7, 2.3, 2.9, 3.7, 4.4, 5.2, 6.5])
    angles.append([ [ 0.07666, [ 3, -0.33333, 0.00000], [ 3, 0.33333, 0.00000]],
                    [ -0.00004, [ 3, -0.33333, 0.07670], [ 3, 0.46667, -0.10738]],
                    [ -1.57699, [ 3, -0.46667, 0.10738], [ 3, 0.36667, -0.08437]],
                    [ -1.66136, [ 3, -0.36667, 0.00000], [ 3, 0.43333, 0.00000]],
                    [ -1.19963, [ 3, -0.43333, 0.00000], [ 3, 0.23333, 0.00000]],
                    [ -1.59847, [ 3, -0.23333, 0.00000], [ 3, 0.36667, 0.00000]],
                    [ -0.32218, [ 3, -0.36667, 0.00000], [ 3, 0.43333, 0.00000]],
                    [ -0.71028, [ 3, -0.43333, 0.00000], [ 3, 0.36667, 0.00000]],
                    [ -0.4, [ 3, -0.36667, 0.00000], [ 3, 0.00000, 0.00000]]])

    names.append('RKneePitch')
    times.append([0.5, 1.0, 1.7, 2.3, 2.9, 3.7, 4.4, 5.2, 6.5])
    angles.append([ [ -0.07819, [ 3, -0.33333, 0.00000], [ 3, 0.33333, 0.00000]],
                    [ 1.98968, [ 3, -0.33333, -0.06900], [ 3, 0.46667, 0.09660]],
                    [ 2.08628, [ 3, -0.46667, 0.00000], [ 3, 0.36667, 0.00000]],
                    [ 1.74267, [ 3, -0.36667, 0.00000], [ 3, 0.43333, 0.00000]],
                    [ 2.12019, [ 3, -0.43333, 0.00000], [ 3, 0.23333, 0.00000]],
                    [ 2.12019, [ 3, -0.23333, 0.00000], [ 3, 0.36667, 0.00000]],
                    [ 2.12019, [ 3, -0.36667, 0.00000], [ 3, 0.43333, 0.00000]],
                    [ 2.12019, [ 3, -0.43333, 0.00000], [ 3, 0.36667, 0.00000]],
                    [ 0.95, [ 3, -0.36667, 0.00000], [ 3, 0.00000, 0.00000]]])

    names.append('RAnklePitch')
    times.append([0.5, 1.0, 1.7, 2.3, 2.9, 3.7, 4.4, 5.2, 6.5])
    angles.append([ [ 0.92965, [ 3, -0.33333, 0.00000], [ 3, 0.33333, 0.00000]],
                    [ -1.02974, [ 3, -0.33333, 0.07746], [ 3, 0.46667, -0.10844]],
                    [ -1.13819, [ 3, -0.46667, 0.02925], [ 3, 0.36667, -0.02298]],
                    [ -1.18645, [ 3, -0.36667, 0.00000], [ 3, 0.43333, 0.00000]],
                    [ -1.18645, [ 3, -0.43333, 0.00000], [ 3, 0.23333, 0.00000]],
                    [ -0.58901, [ 3, -0.23333, 0.00000], [ 3, 0.36667, 0.00000]],
                    [ -1.18645, [ 3, -0.36667, 0.00000], [ 3, 0.43333, 0.00000]],
                    [ -1.18645, [ 3, -0.43333, 0.00000], [ 3, 0.36667, 0.00000]],
                    [ -0.55, [ 3, -0.36667, 0.00000], [ 3, 0.00000, 0.00000]]])

    names.append('RAnkleRoll')
    times.append([0.5, 1.0, 1.7, 2.3, 2.9, 3.7, 4.4, 5.2, 6.5])
    angles.append([ [ 0.18850, [ 3, -0.33333, 0.00000], [ 3, 0.33333, 0.00000]],
                    [ 0.00004, [ 3, -0.33333, 0.00000], [ 3, 0.46667, 0.00000]],
                    [ 0.00618, [ 3, -0.46667, 0.00000], [ 3, 0.36667, 0.00000]],
                    [ -0.00456, [ 3, -0.36667, 0.01074], [ 3, 0.43333, -0.01269]],
                    [ -0.09813, [ 3, -0.43333, 0.00000], [ 3, 0.23333, 0.00000]],
                    [ -0.01376, [ 3, -0.23333, 0.00000], [ 3, 0.36667, 0.00000]],
                    [ -0.09507, [ 3, -0.36667, 0.00000], [ 3, 0.43333, 0.00000]],
                    [ 0.03532, [ 3, -0.43333, -0.02825], [ 3, 0.36667, 0.02390]],
                    [ 0.0, [ 3, -0.36667, 0.00000], [ 3, 0.00000, 0.00000]]])
    
    motProxy.angleInterpolationBezier(names, times, angles)
    posProxy.goToPosture("StandInit", 0.5)

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
        backToStand(motProxy, posProxy)
        motProxy.walkTo(0.1, 0.05, 1.5)

    elif posProxy.getPosture() == 'Belly':
        bellyToStand(motProxy, posProxy)
        motProxy.walkTo(-0.1, -0.05, -1.5)
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
