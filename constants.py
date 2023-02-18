import numpy as np

showErrors = False

gravity = -9.8
maxForce = 100
iterations = 500

kickBallStartingPosition = [-2.5, 0.0, 0.5]
targetBallStartingPosition = [-5.0, 0.0, 0.5]

numberOfGenerations = 1
populationSize = 1

numLegs = 4
legNames = ['Front', 'Back', 'Right', 'Left']
# numLegs = 8
# legNames = ['Front', 'Back', 'Right', 'Left', 'FrontRight', 'FrontLeft', 'BackRight', 'BackLeft']

fitness = "kickBall" # can be kickBall, distance, jumping, target

oscillatory = False # can be True or False
x = 22.2 # frequency of oscillation

numSensorNeurons = numLegs + 1
numMotorNeurons = numLegs * 2
numHiddenNeurons = 0

motorJointRange = 0.22
