import numpy as np

gravity = -9.8
maxForce = 100
iterations = 1000

numberOfGenerations = 10
populationSize = 10

numLegs = 4
legNames = ['Front', 'Back', 'Right', 'Left']
# numLegs = 8
# legNames = ['Front', 'Back', 'Right', 'Left', 'FrontRight', 'FrontLeft', 'BackRight', 'BackLeft']

fitness = "jumping"
# fitness = "distance"

oscillatory = True
# oscillatory = False

numSensorNeurons = numLegs + 1
numMotorNeurons = numLegs * 2
numHiddenNeurons = 12

motorJointRange = 0.2
x = 22.2