import numpy as np
import pyrosim.pyrosim as pyrosim
import os
import random
import time
import constants as c

class SOLUTION:

    def __init__(self, id):
        self.myID = id
        self.numlinks = random.randint(2, 10)
        self.sensorValues = np.random.randint(2, size=self.numlinks) # random array of 0s and 1s. 1 means sensor, 0 means no sensor
        self.numSensors = np.sum(self.sensorValues)
        self.numMotors = self.numlinks - 1
        self.weights = np.random.rand(self.numSensors, self.numMotors) * 2 - 1 # matrix of vals between -1 and 1. Row i, col j is synapse weight between sensor i and motor j
        self.Create_World()
        self.Create_Body()
        self.Create_Brain()

    def Set_ID(self, id):
        self.myID = id
    
    # create the brain, simulate in background
    def Start_Simulation(self, directOrGUI):
        self.Create_Brain()
        if c.showErrors:
            os.system(f"start /B python simulate.py {directOrGUI} {self.myID}") 
        else:
            os.system(f"start /B python simulate.py {directOrGUI} {self.myID} >nul 2>&1")
        
    # once the simulation is over, read in the fitness and delete that file
    def Wait_For_Simulation_To_End(self):
        while not os.path.exists(f"fitness{self.myID}.txt"):
            time.sleep(0.01)
        f = open(f"fitness{self.myID}.txt", "r")
        self.fitness = float(f.read())
        f.close()
        os.system(f"del fitness{self.myID}.txt")

    # pick a random weight and change it to a random value
    def Mutate(self):
        if c.numHiddenNeurons == 0:
            self.weights[random.randint(0, c.numSensorNeurons-1)][random.randint(0, c.numMotorNeurons-1)] = random.random()*2 - 1
        else:
            if random.randint(0, 1) < 0.5:
                self.sensorToHiddenWeights[random.randint(0, c.numSensorNeurons-1)][random.randint(0, c.numHiddenNeurons-1)] = random.random()*2 - 1
            else:
                self.hiddenToMotorWeights[random.randint(0, c.numHiddenNeurons-1)][random.randint(0, c.numMotorNeurons-1)] = random.random()*2 - 1

    def Create_Brain(self):
        pyrosim.Start_NeuralNetwork(f"brain{self.myID}.nndf")

        # create sensor neurons
        sensorCounter = 0
        for i in range(self.numlinks):
            if self.sensorValues[i] == 1:
                pyrosim.Send_Sensor_Neuron(name=f"Sensor{sensorCounter}", linkName=f"Link{i}")
                sensorCounter += 1
        
        # create motor neurons
        for i in range(self.numMotors):
            pyrosim.Send_Motor_Neuron(name=f"Motor{i}", jointName=f"Link{i}_Link{i+1}")

        # create synpases
        for i in range(self.numSensors):
            for j in range(self.numMotors):
                pyrosim.Send_Synapse(f"Sensor{i}", f"Motor{j}", self.weights[i][j])

        pyrosim.End()

    def Create_World(self):
        pyrosim.Start_SDF("world.sdf")
        pyrosim.End()

    def Create_Body(self):
        pyrosim.Start_URDF("body.urdf")

        # first link is the root, with absolute position
        xpos = 0
        ypos = 0
        xrad = random.random() * 0.5 + 0.125          # x radius between 0.125 and 0.625
        yrad = random.random() * 0.5 + 0.125          # y radius between 0.125 and 0.625
        zrad = random.random() * 0.5 + 0.125          # z radius between 0.125 and 0.625
        if self.sensorValues[0] == 0:
            pyrosim.Send_Cube(name="Link0", pos=[xpos, ypos, 0.625], size=[xrad*2, yrad*2, zrad*2], color="Cyan") # no sensor
        else:
            pyrosim.Send_Cube(name="Link0", pos=[xpos, ypos, 0.625], size=[xrad*2, yrad*2, zrad*2], color="Green") # yes sensor
        pyrosim.Send_Joint(name="Link0_Link1", parent="Link0", child="Link1", type="revolute", position=[0, yrad, 0.625], jointAxis="1 0 0")

        # loop through to create the remainder of the links
        for i in range(1, self.numlinks):
            if i != 1:
                # add a joint from previous link to this next link. Position relative to previous joint
                pyrosim.Send_Joint(name=f"Link{i-1}_Link{i}", parent=f"Link{i-1}", child=f"Link{i}", type="revolute", position=[0, yrad*2, 0], jointAxis="1 0 0")

            # add a link 
            xrad = random.random() * 0.5 + 0.125          # x radius between 0.125 and 0.625
            yrad = random.random() * 0.5 + 0.125          # y radius between 0.125 and 0.625
            zrad = random.random() * 0.5 + 0.125          # z radius between 0.125 and 0.625
            if self.sensorValues[i] == 0:
                pyrosim.Send_Cube(name=f"Link{i}", pos=[0, yrad, 0], size=[xrad*2, yrad*2, zrad*2], color="Cyan") # no sensor
            else:
                pyrosim.Send_Cube(name=f"Link{i}", pos=[0, yrad, 0], size=[xrad*2, yrad*2, zrad*2], color="Green") # yes sensor

        pyrosim.End()


    
