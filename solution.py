import numpy as np
import pyrosim.pyrosim as pyrosim
import os
import random
import time
import constants as c

class SOLUTION:

    def __init__(self, id):
        self.myID = id
        self.currentLinkNumber = 0
        self.maxLinks = 50
        self.pExtend = 0.9
        self.pTurn = 0.1
        self.pSensor = 0.5 # odds a link contains a sensor
        self.pMotor = 0.5 # odds a joint has a motor
        self.sensors = [] # contains numbers that represent which links will have sensors
        self.motors = [] # contains tuples (l1, l2, axis) that represent a joint between links l1 and l2 around axis
        self.directionToProbability = {
            tuple([1, 0, 0]): (self.pExtend, 0, self.pTurn, self.pTurn, self.pTurn, self.pTurn),
            tuple([-1, 0, 0]): (0, self.pExtend, self.pTurn, self.pTurn, self.pTurn, self.pTurn),
            tuple([0, 1, 0]): (self.pTurn, self.pTurn, self.pExtend, 0, self.pTurn, self.pTurn),
            tuple([0, -1, 0]): (self.pTurn, self.pTurn, 0, self.pExtend, self.pTurn, self.pTurn),
            tuple([0, 0, 1]): (self.pTurn, self.pTurn, self.pTurn, self.pTurn, self.pExtend, 0),
            tuple([0, 0, -1]): (self.pTurn, self.pTurn, self.pTurn, self.pTurn, 0, self.pExtend)
        }
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

        # create weights between neurons depending on how many there are
        self.weights = np.random.random((len(self.sensors), len(self.motors))) * 2 - 1

        # create sensor neurons
        for i in self.sensors:
            pyrosim.Send_Sensor_Neuron(name=f"Sensor{i}", linkName=f"Link{i}")
        
        # create motor neurons
        for tup in self.motors:
            pyrosim.Send_Motor_Neuron(name=f"Motor{tup[0]}_{tup[1]}", jointName=f"Link{tup[0]}_Link{tup[1]}")

        # create synpases
        i = 0
        for s in self.sensors:
            j = 0
            for tup in self.motors:
                pyrosim.Send_Synapse(f"Sensor{s}", f"Motor{tup[0]}_{tup[1]}", self.weights[i][j])
                j += 1
            i += 1

        pyrosim.End()

    def Create_World(self):
        pyrosim.Start_SDF("world.sdf")
        pyrosim.End()

    def Create_Body(self):  
        pyrosim.Start_URDF("body.urdf")

        # first link is the root, with absolute position
        radii = self.Get_Radii()
        color = "Cyan"
        if random.random() < self.pSensor:
            color = "Green"
            self.sensors.append(self.currentLinkNumber)
        pyrosim.Send_Cube(name=f"Link{self.currentLinkNumber}", pos=[0, 0, 0.125], size=2*radii, color=color)
        self.currentLinkNumber += 1

        # utilize recursive function to make the rest of the body
        self.Make_Limb(self.currentLinkNumber-1, [0, 0, 0.125 + radii[2]], [0, 0, 1], 0.125 + radii[2])
        
        pyrosim.End()

    # takes [x, y, z] as jointPos and [0, 0, 0] but replace one 0 with +/- 1 for direction
    def Make_Limb(self, prevLinkNumber, jointPos, direction, globalZ):
        if self.currentLinkNumber > self.maxLinks - 1: # to stop the recursion
            return

        if globalZ < 0.125: # under the ground
            return

        # first make a joint from the previous link to the new one you are about to create
        pyrosim.Send_Joint(name=f"Link{prevLinkNumber}_Link{self.currentLinkNumber}", parent=f"Link{prevLinkNumber}", child=f"Link{self.currentLinkNumber}", type="revolute", position=jointPos, jointAxis="1 0 0")
        if random.random() < self.pMotor:
            self.motors.append((prevLinkNumber, self.currentLinkNumber))

        # make a new limb by getting a size, calculating the position it should be relative to previous
        radii = self.Get_Radii()
        linkPos = np.multiply(direction, radii)
        color = "Cyan"
        if random.random() < self.pSensor:
            color = "Green"
            self.sensors.append(self.currentLinkNumber)
        pyrosim.Send_Cube(name=f"Link{self.currentLinkNumber}", pos=linkPos, size=2*radii, color=color)
        myLinkNumber = self.currentLinkNumber
        self.currentLinkNumber += 1

        # use recursion to make more limbs
        self.Random_Limb(direction, myLinkNumber, radii, self.directionToProbability[tuple(direction)], globalZ) # right
        

    # given probabilities [right, left, up, down, forward, back], create random limbs
    def Random_Limb(self, direction, linkNum, radii, probabilities, globalZ):

        # loop through all the possible directions to create a link, if the random number says make it, do it using fun math
        i = 0
        for key in self.directionToProbability.keys():
            if (random.random() < probabilities[i]):
                jointPos = np.multiply(np.add(direction, list(key)), radii)
                self.Make_Limb(linkNum, jointPos, list(key), globalZ + jointPos[2])
            i += 1

    # returns an array of random radii between 0.125 and 0.625 like [x, y, z] so that the length of each side is between 0.25 and 1.25
    def Get_Radii(self):
        return np.array([0.125, 0.125, 0.125])




    


    
