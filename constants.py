import numpy as np

showErrors = False

gravity = -9.8
maxForce = 100
iterations = 1000

kickBallStartingPosition = [-2.5, 0.0, 0.5]

numberOfGenerations = 10
populationSize = 10

numLegs = 4
legNames = ['Front', 'Back', 'Right', 'Left']
# numLegs = 8
# legNames = ['Front', 'Back', 'Right', 'Left', 'FrontRight', 'FrontLeft', 'BackRight', 'BackLeft']

fitness = "kickBall" # can be kickBall, distance, or jumping

oscillatory = False # can be True or False

numSensorNeurons = numLegs + 1
numMotorNeurons = numLegs * 2
numHiddenNeurons = 12

motorJointRange = 0.22
x = 22.2