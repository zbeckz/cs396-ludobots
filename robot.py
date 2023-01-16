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

    def Prepare_To_Sense(self):
        self.sensors = {}
        for linkName in pyrosim.linkNamesToIndices:
            self.sensors[linkName] = SENSOR(linkName)

    def Sense(self, step):
        counter = 0
        for sensor in self.sensors.values():
            sensor.Get_Value(step, counter)
            counter += 1

    def Prepare_To_Act(self):
        self.motors = {}
        for jointName in pyrosim.jointNamesToIndices:
            self.motors[jointName] = MOTOR(jointName)

    def Act(self, step):
        for neuronName in self.nn.Get_Neuron_Names():
            if self.nn.Is_Motor_Neuron(neuronName):
                jointName = self.nn.Get_Motor_Neurons_Joint(neuronName)
                desiredAngle = self.nn.Get_Value_Of(neuronName) * c.motorJointRange
                self.motors[jointName].Set_Value(self.robotId, desiredAngle)
                
    def Think(self):
        self.nn.Update()

    def Get_Fitness(self, id):
        fitness = self.__jumpingFitnessEightLegs()
        f = open(f"tmp{id}.txt", "w")
        f.write(str(fitness))
        f.close()
        os.rename(f"tmp{id}.txt", f"fitness{id}.txt")

    # param 0 means x, 1 means y, 2 means z
    def __distanceFitness(self, param):
        return p.getBasePositionAndOrientation(self.robotId)[0][param]

    # returns the length of longest chain where all legs sensors are -1 (not touching the ground)
    def __jumpingFitnessFourLegs(self):
        longestRun = 0
        currentRun = 0
        for i in range(c.iterations):
            if self.sensors["FrontLowerLeg"].values[i] == -1 and self.sensors["BackLowerLeg"].values[i] == -1 and self.sensors["RightLowerLeg"].values[i] == -1 and self.sensors["LeftLowerLeg"].values[i] == -1:
                currentRun += 1
            else:
                if currentRun > longestRun:
                    longestRun = currentRun
                currentRun = 0

        if currentRun > longestRun:
            return currentRun
        else:
            return longestRun

    def __jumpingFitnessEightLegs(self):
        longestRun = 0
        currentRun = 0
        for i in range(c.iterations):
            if self.sensors["FrontLowerLeg"].values[i] == -1 and self.sensors["BackLowerLeg"].values[i] == -1 and self.sensors["RightLowerLeg"].values[i] == -1 and self.sensors["LeftLowerLeg"].values[i] == -1 and self.sensors["FrontRightLowerLeg"].values[i] == -1 and self.sensors["FrontLeftLowerLeg"].values[i] == -1 and self.sensors["BackRightLowerLeg"].values[i] == -1 and self.sensors["BackLeftLowerLeg"].values[i] == -1:
                currentRun += 1
            else:
                if currentRun > longestRun:
                    longestRun = currentRun
                currentRun = 0

        if currentRun > longestRun:
            return currentRun
        else:
            return longestRun
