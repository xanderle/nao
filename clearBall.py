from naoqi import ALProxy

def clearBall(motionProxy):
    motionProxy.moveTo(0.5, 0.0, 0.0)
    motionProxy.waitUntilMoveIsFinished()
    motionProxy.moveTo(-0.5, 0.0, 0.0)
    motionProxy.waitUntilMoveIsFinished()
