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
        p.configureDebugVisualizer(p.COV_ENABLE_GUI,0)
        p.setAdditionalSearchPath(pybullet_data.getDataPath())
        p.setGravity(0,0,c.gravity)
        self.world = WORLD()
        self.robot = ROBOT(solID)
        self.kickBallPos = [0] * c.iterations
        self.targetBallPos = [0] * c.iterations

    def Run(self):
        for i in range(c.iterations): 
            p.stepSimulation()
            self.robot.Sense(i)
            self.robot.Think()
            self.robot.Act(i)
            if self.directOrGUI == "GUI":
                time.sleep(1/60)

    def Get_Fitness(self, id):
        if c.fitness == "kickBall":
            self.robot.Get_Fitness(id, self.world.getPosAndOrientation(0)[0])
        elif c.fitness == "target":
            self.robot.Get_Fitness(id=id, ballPos=self.kickBallPos, targetPos=self.targetBallPos)
        else:
            self.robot.Get_Fitness(id)
        

    def __del__(self):
        p.disconnect()