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
    def Get_Fitness(self, id):
        fitness = self.__distanceFitness(0) * -1
        f = open(f"tmp{id}.txt", "w")
        f.write(str(fitness))
        f.close()
        os.rename(f"tmp{id}.txt", f"fitness{id}.txt")

    # param 0 means x, 1 means y, 2 means z
    def __distanceFitness(self, param):
        return p.getBasePositionAndOrientation(self.robotId)[0][param]