from sensor import SENSOR
from motor import MOTOR
import pyrosim.pyrosim as pyrosim
import pybullet as p
from pyrosim.neuralNetwork import NEURAL_NETWORK
import os
import constants as c
import numpy as np

class ROBOT:

    def __init__(self, solID):
        self.robotId = p.loadURDF("body.urdf")
        self.nn = NEURAL_NETWORK(f"brain{solID}.nndf")
        pyrosim.Prepare_To_Simulate(self.robotId)
        self.Prepare_To_Sense()
        self.Prepare_To_Act()
        os.system(f"del brain{solID}.nndf")

    # generate the sensors
    def Prepare_To_Sense(self):
        self.sensors = {}
        for linkName in pyrosim.linkNamesToIndices:
            self.sensors[linkName] = SENSOR(linkName)

    # tell each sensor to check its value
    def Sense(self, step):
        counter = 0
        for sensor in self.sensors.values():
            sensor.Get_Value(step, counter) # counter to tell the sensor function what sensor it is
            counter += 1

    # generate the motors
    def Prepare_To_Act(self):
        self.motors = {}
        for jointName in pyrosim.jointNamesToIndices:
            self.motors[jointName] = MOTOR(jointName)

    # move joints based on motor neuron values
    def Act(self, step):
        for neuronName in self.nn.Get_Neuron_Names():
            if self.nn.Is_Motor_Neuron(neuronName):
                jointName = self.nn.Get_Motor_Neurons_Joint(neuronName)
                desiredAngle = self.nn.Get_Value_Of(neuronName) * c.motorJointRange
                self.motors[jointName].Set_Value(self.robotId, desiredAngle)
                
    def Think(self):
        self.nn.Update()

    # calculate fitness value and write to a file
    def Get_Fitness(self, id, ballPos):
        if c.fitness == "jumping":
            fitness = self.__jumpingFitness(c.numLegs) # jumping with either 4 or 8 legs
        elif c.fitness == "distance":
            fitness = self.__distanceFitness(0) * -1
        else:
            fitness = self.__kickBallFitness(ballPos)
        f = open(f"tmp{id}.txt", "w")
        f.write(str(fitness))
        f.close()
        os.rename(f"tmp{id}.txt", f"fitness{id}.txt")

    # the sphere should end up as far away from its starting position as possible, param 0 means x, 1 means 1, 2 means z
    def __kickBallFitness(self, ballPosTuple):
        ballPos = [ballPosTuple[0], ballPosTuple[1], ballPosTuple[2]]
        ballPosDist = np.sqrt((c.kickBallStartingPosition[0] - ballPos[0])**2 + (c.kickBallStartingPosition[1] - ballPos[1])**2 + (c.kickBallStartingPosition[2] - ballPos[2])**2)
        robotPos = p.getBasePositionAndOrientation(self.robotId)[0]
        fit = np.sqrt((robotPos[0] - ballPos[0])**2 + (robotPos[1] - ballPos[1])**2 + (robotPos[2] - ballPos[2])**2) 
        if ballPosDist < 0.05:
            fit = fit * -1 # if it hasn't moved the ball, then fitness distance should be negative so that closer to the ball is better
        return fit # otherwise, the further the ball the better, so return the distance from the robot to the ball

    # param 0 means x, 1 means y, 2 means z
    def __distanceFitness(self, param):
        return p.getBasePositionAndOrientation(self.robotId)[0][param]

    # returns the length of longest chain where all legs sensors are -1 (not touching the ground)
    def __jumpingFitness(self, legs):
        longestRun = 0
        currentRun = 0
        for i in range(c.iterations):
            if self.__jumpingCondition(i, legs):
                currentRun += 1
            else:
                if currentRun > longestRun:
                    longestRun = currentRun
                currentRun = 0

        if currentRun > longestRun:
            return currentRun
        else:
            return longestRun

    def __jumpingCondition(self, i, legs):
        if legs == 4:
            return self.sensors["FrontLowerLeg"].values[i] == -1 and self.sensors["BackLowerLeg"].values[i] == -1 and self.sensors["RightLowerLeg"].values[i] == -1 and self.sensors["LeftLowerLeg"].values[i] == -1
        else:
            return self.sensors["FrontLowerLeg"].values[i] == -1 and self.sensors["BackLowerLeg"].values[i] == -1 and self.sensors["RightLowerLeg"].values[i] == -1 and self.sensors["LeftLowerLeg"].values[i] == -1 and self.sensors["FrontRightLowerLeg"].values[i] == -1 and self.sensors["FrontLeftLowerLeg"].values[i] == -1 and self.sensors["BackRightLowerLeg"].values[i] == -1 and self.sensors["BackLeftLowerLeg"].values[i] == -1
