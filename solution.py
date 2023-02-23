import numpy as np
import pyrosim.pyrosim as pyrosim
import os
import random
import time
import constants as c
import math

class SOLUTION:

    def __init__(self, id):
        self.myID = id
        self.globalTorsoNumber = 0
        self.globalLegNumber = 0
        self.globalBodyNumber = 0
        self.globalFootNumber = 0
        self.sensorNeurons = [] # contains the feet numbers to add sensor neurons to
        self.motorNeurons = [] # contains the joint names to add motor neurons to
        self.weights = {}

        # torso links are ones that have 2 legs coming out of them
        self.torsoSpecs = {
            "num": random.randint(1, 5),           # number of torso links in the whole thing
            "x": random.random() * 0.25 + 0.12,             # in the form of radii, not diameter
            "y": random.random() * 0.25 + 0.02,
            "z": random.random() * 0.25 + 0.02
        }

        # body links are ones that connect torso pieces, have no legs
        self.bodySpecs = {
            "num": random.randint(0, 2),           # number of body links between torso links
            "x": random.random() * 0.25 + 0.12,
            "y": random.random() * 0.25 + 0.02,
            "z": random.random() * 0.25 + 0.02
        }

        # leg links are ones that come out of torso links horizontally
        self.legSpecs = {
            "num": random.randint(1, 3),           # number of leg links per limb, horizontal links
            "x": random.random() * 0.25 + 0.02,
            "y": random.random() * 0.25 + 0.06,
            "z": random.random() * 0.25 + 0.02
        }

        self.footSpecs = {
            "num": random.randint(1, 3),           # number of foot links per limb, vertical links
            "x": random.random() * 0.25 + 0.02,
            "y": random.random() * 0.25 + 0.02,
            "z": random.random() * 0.25 + 0.06
        }

        # this is done so that the creature starts with its lowest point touching the ground
        self.startHeight = self.footSpecs["num"]*2*self.footSpecs["z"]
        if self.torsoSpecs["z"] > self.startHeight: self.startHeight = self.torsoSpecs["z"]
        if self.bodySpecs["z"] > self.startHeight: self.startHeight = self.bodySpecs["z"]
        if self.legSpecs["z"] > self.startHeight: self.startHeight = self.legSpecs["z"]
            
        self.Create_World()
        self.Create_Body()
        self.Create_Brain(True)

    def Set_ID(self, id):
        self.myID = id
    
    # create the brain, simulate in background
    def Start_Simulation(self, directOrGUI):
        self.Create_Brain(False)
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
        self.Mutate_Body()
        self.Mutate_Brain()

    def Mutate_Body(self):
        pass

    def Mutate_Brain(self):
        pass

    def Create_Brain(self, first):
        pyrosim.Start_NeuralNetwork(f"brain{self.myID}.nndf")

        # create a sensor neuron in each foot
        for i in range(len(self.sensorNeurons)):
            pyrosim.Send_Sensor_Neuron(f"sensor{i}", f"foot{self.sensorNeurons[i]}")

        # create motor neurons in each joint
        for i in range(len(self.motorNeurons)):
            pyrosim.Send_Motor_Neuron(f"motor{i}", self.motorNeurons[i])

        # connect each sensor neurons to the motor joints along its corresponding torso and the body joints
        legAndFeetJoints = 2 * (self.legSpecs["num"] + self.footSpecs["num"])
        bodyAndTorsoJoints = 1 + self.bodySpecs["num"]
        for i in range(len(self.sensorNeurons)):
            multiplier = math.floor(i/2)
            increment = multiplier * (legAndFeetJoints + bodyAndTorsoJoints)
            start = increment
            end = increment + legAndFeetJoints + bodyAndTorsoJoints
            if multiplier != 0: start -= bodyAndTorsoJoints
            if multiplier == self.torsoSpecs["num"] - 1: end -= bodyAndTorsoJoints
            for j in range(start, end):
                if first:
                    w = random.random() * 2 - 1
                    self.weights[(i, j)] = w
                else:
                    w = self.weights[(i, j)]
                pyrosim.Send_Synapse(f"sensor{i}", f"motor{j}", w)

        pyrosim.End()

    def Create_World(self):
        pyrosim.Start_SDF("world.sdf")
        pyrosim.End()

    def Create_Body(self):  
        pyrosim.Start_URDF("body.urdf")

        # start by creating a torso link, position is global because root
        # the torso function will call other functions to create the body, so this is all we need to do, yay!
        self.Create_Torso_Link([0, 0, self.startHeight])
        
        pyrosim.End()

    # create a torso link and call the functions to create legs / body if necessary
    def Create_Torso_Link(self, position):

        # create the torso link
        pyrosim.Send_Cube(name=f"torso{self.globalTorsoNumber}", pos=position, size=[2*self.torsoSpecs["x"], 2*self.torsoSpecs["y"], 2*self.torsoSpecs["z"]], color="cyan")
        self.globalTorsoNumber += 1

        # create joints and call the function to create the legs
        for i in (1, -1): # to create one leg in front and one behind the torso
            jointPos = [self.torsoSpecs["x"], i*self.torsoSpecs["y"], 0]
            if self.globalTorsoNumber == 1: 
                jointPos[2] = self.startHeight # first torso means the joint positions are absolute, not relative
                jointPos[0] = 0
            pyrosim.Send_Joint(name=f"torso{self.globalTorsoNumber-1}_leg{self.globalLegNumber}", parent=f"torso{self.globalTorsoNumber-1}", child=f"leg{self.globalLegNumber}", type="revolute" ,position=jointPos, jointAxis="1 0 0")
            self.motorNeurons.append(f"torso{self.globalTorsoNumber-1}_leg{self.globalLegNumber}")
            self.Create_Leg_Link([0, i*self.legSpecs["y"], 0], 0, i)

        # if not all torso links have been created, create either the next body link or the next torso link
        if self.globalTorsoNumber < self.torsoSpecs["num"]:
            jointPos = [2*self.torsoSpecs["x"], 0, 0]
            if self.globalTorsoNumber == 1: # first torso link means joint position is absolute, not relative
                jointPos[2] = self.startHeight
                jointPos[0] = self.torsoSpecs["x"]
            if self.bodySpecs["num"] != 0: # create a body link
                pyrosim.Send_Joint(name=f"torso{self.globalTorsoNumber-1}_body{self.globalBodyNumber}", parent=f"torso{self.globalTorsoNumber-1}", child=f"body{self.globalBodyNumber}", type="revolute", position=jointPos, jointAxis="0 0 1")
                self.motorNeurons.append(f"torso{self.globalTorsoNumber-1}_body{self.globalBodyNumber}")
                self.Create_Body_Link([self.bodySpecs["x"], 0, 0], 0)
            else: # create next torso link
                pyrosim.Send_Joint(name=f"torso{self.globalTorsoNumber-1}_torso{self.globalTorsoNumber}", parent=f"torso{self.globalTorsoNumber-1}", child=f"torso{self.globalTorsoNumber}", type="revolute", position=jointPos, jointAxis="0 0 1")
                self.motorNeurons.append(f"torso{self.globalTorsoNumber-1}_torso{self.globalTorsoNumber}")
                self.Create_Torso_Link([self.torsoSpecs["x"], 0, 0])

    def Create_Body_Link(self, position, localBodyNum):

        # create body link
        pyrosim.Send_Cube(name=f"body{self.globalBodyNumber}", pos=position, size=[2*self.bodySpecs["x"], 2*self.bodySpecs["y"], 2*self.bodySpecs["z"]], color="cyan")
        self.globalBodyNumber += 1

        # if not all body links have been created, create the next one. otherwise, create the next torso
        jointPos = [2*self.bodySpecs["x"], 0, 0]
        if localBodyNum < self.bodySpecs["num"] - 1:
            pyrosim.Send_Joint(name=f"body{self.globalBodyNumber - 1}_body{self.globalBodyNumber}", parent=f"body{self.globalBodyNumber-1}", child=f"body{self.globalBodyNumber}", type="revolute", position=jointPos, jointAxis="0 0 1")
            self.motorNeurons.append(f"body{self.globalBodyNumber - 1}_body{self.globalBodyNumber}")
            self.Create_Body_Link([self.bodySpecs["x"], 0, 0], localBodyNum + 1)
        else: # otherwise create the next torso link
            pyrosim.Send_Joint(name=f"body{self.globalBodyNumber - 1}_torso{self.globalTorsoNumber}", parent=f"body{self.globalBodyNumber-1}", child=f"torso{self.globalTorsoNumber}", type="revolute", position=jointPos, jointAxis="0 0 1")
            self.motorNeurons.append(f"body{self.globalBodyNumber - 1}_torso{self.globalTorsoNumber}")
            self.Create_Torso_Link([self.torsoSpecs["x"], 0, 0])

    def Create_Leg_Link(self, position, localLegNum, multiplier):

        # create the leg link
        pyrosim.Send_Cube(name=f"leg{self.globalLegNumber}", pos=position, size=[2*self.legSpecs["x"], 2*self.legSpecs["y"], 2*self.legSpecs["z"]], color="cyan")
        self.globalLegNumber += 1

        # if not all leg links have been created, create the next one
        yPos = multiplier * self.legSpecs["y"] # used in either case
        if localLegNum < self.legSpecs["num"] - 1:
            pyrosim.Send_Joint(name=f"leg{self.globalLegNumber-1}_leg{self.globalLegNumber}", parent=f"leg{self.globalLegNumber-1}", child=f"leg{self.globalLegNumber}", type="revolute", position=[0, 2*yPos, 0], jointAxis="1 0 0")
            self.motorNeurons.append(f"leg{self.globalLegNumber-1}_leg{self.globalLegNumber}")
            self.Create_Leg_Link([0, yPos, 0], localLegNum+1, multiplier)
        else: # otherwise, create the first foot
            pyrosim.Send_Joint(name=f"leg{self.globalLegNumber-1}_foot{self.globalFootNumber}", parent=f"leg{self.globalLegNumber-1}", child=f"foot{self.globalFootNumber}", type="revolute", position=[0, 2*yPos, 0], jointAxis="0 1 0")
            self.motorNeurons.append(f"leg{self.globalLegNumber-1}_foot{self.globalFootNumber}")
            self.Create_Foot_Link([0, 0, -1 * self.footSpecs["z"]], 0)

    def Create_Foot_Link(self, position, localFootNum):
        
        # create the foot link
        color = "Cyan"
        if localFootNum == self.footSpecs["num"] - 1: # bottom foot
            color = "Green"
            self.sensorNeurons.append(self.globalFootNumber)
        pyrosim.Send_Cube(name=f"foot{self.globalFootNumber}", pos=position, size=[2*self.footSpecs["x"], 2*self.footSpecs["y"], 2*self.footSpecs["z"]], color=color)
        self.globalFootNumber += 1

        # if not all foot links have been created, create the next one
        if localFootNum < self.footSpecs["num"] - 1:
            pyrosim.Send_Joint(name=f"foot{self.globalFootNumber-1}_foot{self.globalFootNumber}", parent=f"foot{self.globalFootNumber-1}", child=f"foot{self.globalFootNumber}", type="revolute", position=[0, 0, -2 * self.footSpecs["z"]], jointAxis="0 1 0")
            self.motorNeurons.append(f"foot{self.globalFootNumber-1}_foot{self.globalFootNumber}")
            self.Create_Foot_Link([0, 0, -1 * self.footSpecs["z"]], localFootNum+1)

