import numpy as np
import pyrosim.pyrosim as pyrosim
import os
import random
import time
import constants as c

class SOLUTION:

    def __init__(self, id):
        self.myID = id
        self.globalTorsoNumber = 0
        self.globalLegNumber = 0
        self.globalBodyNumber = 0
        self.globalFootNumber = 0

        # torso links are ones that have 2 legs coming out of them
        self.torsoSpecs = {
            "num": 3,           # number of torso links in the whole thing
            "x": 0.25,             # in the form of radii, not diameter
            "y": 0.125,
            "z": 0.0625
        }

        # body links are ones that connect torso pieces, have no legs
        self.bodySpecs = {
            "num": 1,           # number of body links between torso links
            "x": 0.25,
            "y": 0.125,
            "z": 0.0625
        }

        # leg links are ones that come out of torso links horizontally
        self.legSpecs = {
            "num": 1,           # number of leg links per limb, horizontal links
            "x": 0.0625,
            "y": 0.1875,
            "z": 0.03125
        }

        self.footSpecs = {
            "num": 1,           # number of foot links per limb, vertical links
            "x": 0.0625,
            "y": 0.03125,
            "z": 0.1875
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
        pass

    def Create_Brain(self):
        pyrosim.Start_NeuralNetwork(f"brain{self.myID}.nndf")

        # # create weights between neurons depending on how many there are
        # self.weights = np.random.random((len(self.sensors), len(self.motors))) * 2 - 1

        # # create sensor neurons
        # for i in self.sensors:
        #     pyrosim.Send_Sensor_Neuron(name=f"Sensor{i}", linkName=f"Link{i}")
        
        # # create motor neurons
        # for tup in self.motors:
        #     pyrosim.Send_Motor_Neuron(name=f"Motor{tup[0]}_{tup[1]}", jointName=f"Link{tup[0]}_Link{tup[1]}")

        # # create synpases
        # i = 0
        # for s in self.sensors:
        #     j = 0
        #     for tup in self.motors:
        #         pyrosim.Send_Synapse(f"Sensor{s}", f"Motor{tup[0]}_{tup[1]}", self.weights[i][j])
        #         j += 1
        #     i += 1

        pyrosim.End()

    def Create_World(self):
        pyrosim.Start_SDF("world.sdf")
        pyrosim.End()

    def Create_Body(self):  
        pyrosim.Start_URDF("body.urdf")

        # start by creating a torso link, position is global because root
        # height is chosen such that the bottom of the lower most feet will be at z = 0
        # the torso function will call other functions to create the body, so this is all we need to do, yay!
        self.startHeight = self.footSpecs["num"]*2*self.footSpecs["z"]
        self.Create_Torso_Link([0, 0, self.startHeight])
        
        pyrosim.End()

    # create a torso link and call the functions to create legs / body if necessary
    def Create_Torso_Link(self, position):

        # create the torso link
        pyrosim.Send_Cube(name=f"torso{self.globalTorsoNumber}", pos=position, size=[2*self.torsoSpecs["x"], 2*self.torsoSpecs["y"], 2*self.torsoSpecs["z"]], color="cyan")
        self.globalTorsoNumber += 1

        # create joints and call the function to create the legs
        for i in [1, -1]: # to create one leg in front and one behind the torso
            jointPos = [self.torsoSpecs["x"], i*self.torsoSpecs["y"], 0]
            if self.globalTorsoNumber == 1: 
                jointPos[2] = self.startHeight # first torso means the joint positions are absolute, not relative
                jointPos[0] = 0
            pyrosim.Send_Joint(name=f"torso{self.globalTorsoNumber-1}_leg{self.globalLegNumber}", parent=f"torso{self.globalTorsoNumber-1}", child=f"leg{self.globalLegNumber}", type="revolute" ,position=jointPos, jointAxis="1 0 0")
            self.Create_Leg_Link([0, i*self.legSpecs["y"], 0], 0, i)

        # if not all torso links have been created, create either the next body link or the next torso link
        if self.globalTorsoNumber < self.torsoSpecs["num"]:
            jointPos = [2*self.torsoSpecs["x"], 0, 0]
            if self.globalTorsoNumber == 1: # first torso link means joint position is absolute, not relative
                jointPos[2] = self.startHeight
                jointPos[0] = self.torsoSpecs["x"]
            if self.bodySpecs["num"] != 0: # create a body link
                pyrosim.Send_Joint(name=f"torso{self.globalTorsoNumber-1}_body{self.globalBodyNumber}", parent=f"torso{self.globalTorsoNumber-1}", child=f"body{self.globalBodyNumber}", type="revolute", position=jointPos, jointAxis="0 0 1")
                self.Create_Body_Link([self.bodySpecs["x"], 0, 0], 0)
            else: # create next torso link
                pyrosim.Send_Joint(name=f"torso{self.globalTorsoNumber-1}_body{self.globalTorsoNumber}", parent=f"torso{self.globalTorsoNumber-1}", child=f"torso{self.globalTorsoNumber}", type="revolute", position=jointPos, jointAxis="0 0 1")
                self.Create_Torso_Link([self.torsoSpecs["x"], 0, 0])

    def Create_Body_Link(self, position, localBodyNum):

        # create body link
        pyrosim.Send_Cube(name=f"body{self.globalBodyNumber}", pos=position, size=[2*self.bodySpecs["x"], 2*self.bodySpecs["y"], 2*self.bodySpecs["z"]], color="cyan")
        self.globalBodyNumber += 1

        # if not all body links have been created, create the next one. otherwise, create the next torso
        jointPos = [2*self.bodySpecs["x"], 0, 0]
        if localBodyNum < self.bodySpecs["num"] - 1:
            pyrosim.Send_Joint(name=f"body{self.globalBodyNumber - 1}_body{self.globalBodyNumber}", parent=f"body{self.globalBodyNumber-1}", child=f"body{self.globalBodyNumber}", type="revolute", position=jointPos, jointAxis="0 0 1")
            self.Create_Body_Link([self.bodySpecs["x"], 0, 0], localBodyNum + 1)
        else: # otherwise create the next torso link
            pyrosim.Send_Joint(name=f"body{self.globalBodyNumber - 1}_torso{self.globalTorsoNumber}", parent=f"body{self.globalBodyNumber-1}", child=f"torso{self.globalTorsoNumber}", type="revolute", position=jointPos, jointAxis="0 0 1")
            self.Create_Torso_Link([self.torsoSpecs["x"], 0, 0])

    def Create_Leg_Link(self, position, localLegNum, multiplier):

        # create the leg link
        pyrosim.Send_Cube(name=f"leg{self.globalLegNumber}", pos=position, size=[2*self.legSpecs["x"], 2*self.legSpecs["y"], 2*self.legSpecs["z"]], color="cyan")
        self.globalLegNumber += 1

        # if not all leg links have been created, create the next one
        yPos = multiplier * self.legSpecs["y"] # used in either case
        if localLegNum < self.legSpecs["num"] - 1:
            pyrosim.Send_Joint(name=f"leg{self.globalLegNumber-1}_leg{self.globalLegNumber}", parent=f"leg{self.globalLegNumber-1}", child=f"leg{self.globalLegNumber}", type="revolute", position=[0, 2*yPos, 0], jointAxis="1 0 0")
            self.Create_Leg_Link([0, yPos, 0], localLegNum+1, multiplier)
        else: # otherwise, create the first foot
            pyrosim.Send_Joint(name=f"leg{self.globalLegNumber-1}_foot{self.globalFootNumber}", parent=f"leg{self.globalLegNumber-1}", child=f"foot{self.globalFootNumber}", type="revolute", position=[0, 2*yPos, 0], jointAxis="0 1 0")
            self.Create_Foot_Link([0, 0, -1 * self.footSpecs["z"]], 0)

    def Create_Foot_Link(self, position, localFootNum):
        
        # create the foot link
        pyrosim.Send_Cube(name=f"foot{self.globalFootNumber}", pos=position, size=[2*self.footSpecs["x"], 2*self.footSpecs["y"], 2*self.footSpecs["z"]], color="cyan")
        self.globalFootNumber += 1

        # if not all foot links have been created, create the next one
        if localFootNum < self.footSpecs["num"] - 1:
            pyrosim.Send_Joint(name=f"foot{self.globalFootNumber-1}_foot{self.globalFootNumber}", parent=f"foot{self.globalFootNumber-1}", child=f"foot{self.globalFootNumber}", type="revolute", position=[0, 0, -2 * self.footSpecs["z"]], jointAxis="0 1 0")
            self.Create_Foot_Link([0, 0, -1 * self.footSpecs["z"]], localFootNum+1)