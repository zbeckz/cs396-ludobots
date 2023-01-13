import numpy as np
import pyrosim.pyrosim as pyrosim
import os
import random
import time

class SOLUTION:

    def __init__(self, id):
        self.myID = id
        self.weights = np.random.rand(3, 2) * 2 - 1

    def Set_ID(self, id):
        self.myID = id

    def Evaluate(self, directOrGUI):
        self.Create_Brain()
        os.system(f"start /B python simulate.py {directOrGUI} {self.myID}")
        while not os.path.exists(f"fitness{self.myID}.txt"):
            time.sleep(0.01)
        f = open(f"fitness{self.myID}.txt", "r")
        self.fitness = float(f.read())
        f.close()
    
    def Start_Simulation(self, directOrGUI):
        self.Create_Brain()
        os.system(f"start /B python simulate.py {directOrGUI} {self.myID}")

    def Wait_For_Simulation_To_End(self):
        while not os.path.exists(f"fitness{self.myID}.txt"):
            time.sleep(0.01)
        f = open(f"fitness{self.myID}.txt", "r")
        self.fitness = float(f.read())
        f.close()
        os.system(f"del fitness{self.myID}.txt")

    def Mutate(self):
        self.weights[random.randint(0, 2)][random.randint(0, 1)] = random.random()*2 - 1

    def Create_World(self):
        pyrosim.Start_SDF("world.sdf")
        pyrosim.Send_Cube(name="Box", pos=[-5, 5, 0.5] , size=[1,1,1])
        pyrosim.End()   

    def Create_Body(self):
        pyrosim.Start_URDF("body.urdf")
        pyrosim.Send_Cube(name= "Torso", pos=[1.5, 0, 1.5] , size=[1,1,1])
        pyrosim.Send_Joint(name = "Torso_BackLeg", parent= "Torso", child = "BackLeg", type = "revolute", position = [1,0,1])
        pyrosim.Send_Cube(name= "BackLeg", pos=[-0.5, 0, -0.5] , size=[1,1,1])
        pyrosim.Send_Joint(name = "Torso_FrontLeg", parent= "Torso", child = "FrontLeg", type = "revolute", position = [2,0,1])
        pyrosim.Send_Cube(name= "FrontLeg", pos=[0.5, 0, -0.5] , size=[1,1,1])
        pyrosim.End()

    def Create_Brain(self):
        pyrosim.Start_NeuralNetwork(f"brain{self.myID}.nndf")
        
        pyrosim.Send_Sensor_Neuron(name = 0, linkName = "Torso")     
        pyrosim.Send_Sensor_Neuron(name = 1, linkName = "BackLeg")
        pyrosim.Send_Sensor_Neuron(name = 2, linkName = "FrontLeg")
        
        pyrosim.Send_Motor_Neuron(name = 3, jointName = "Torso_BackLeg")
        pyrosim.Send_Motor_Neuron(name = 4, jointName = "Torso_FrontLeg")
    
        for currentRow in range(3):
            for currentCol in range(2):
                pyrosim.Send_Synapse(sourceNeuronName = currentRow, 
                                     targetNeuronName = currentCol + 3, 
                                     weight = self.weights[currentRow][currentCol])
    
        pyrosim.End()