from world import WORLD
from robot import ROBOT
import pybullet as p
import pybullet_data
import pyrosim.pyrosim as pyrosim
import constants as c
import numpy as np
import time

class SIMULATION:

    def __init__(self, directOrGUI, solID):
        self.directOrGUI = directOrGUI
        if self.directOrGUI == "DIRECT":
            self.physicsClient = p.connect(p.DIRECT)
        else:
            self.physicsClient = p.connect(p.GUI)
        p.setAdditionalSearchPath(pybullet_data.getDataPath())
        p.setGravity(0,0,c.gravity)
        self.world = WORLD()
        self.robot = ROBOT(solID)

    def Run(self):
        for i in range(c.iterations): 
            p.stepSimulation()
            self.robot.Sense(i)
            self.robot.Think()
            self.robot.Act(i)
            if self.directOrGUI == "GUI":       
                time.sleep(1/60)

    def Get_Fitness(self, id):
        self.robot.Get_Fitness(id)

    def __del__(self):
        p.disconnect()