import numpy as np
import pyrosim.pyrosim as pyrosim
import os
import random
import time
import constants as c

class SOLUTION:

    def __init__(self, id):
        self.myID = id
        self.weights = np.random.rand(c.numSensorNeurons, c.numMotorNeurons) * 2 - 1

    def Set_ID(self, id):
        self.myID = id

    def Evaluate(self, directOrGUI):
        self.Create_Brain()
        os.system(f"start /B python simulate.py {directOrGUI} {self.myID} >nul 2>&1")
        while not os.path.exists(f"fitness{self.myID}.txt"):
            time.sleep(0.01)
        f = open(f"fitness{self.myID}.txt", "r")
        self.fitness = float(f.read())
        f.close()
    
    def Start_Simulation(self, directOrGUI):
        self.Create_Brain()
        os.system(f"start /B python simulate.py {directOrGUI} {self.myID} >nul 2>&1")

    def Wait_For_Simulation_To_End(self):
        while not os.path.exists(f"fitness{self.myID}.txt"):
            time.sleep(0.01)
        f = open(f"fitness{self.myID}.txt", "r")
        self.fitness = float(f.read())
        f.close()
        os.system(f"del fitness{self.myID}.txt")

    def Mutate(self):
        self.weights[random.randint(0, c.numSensorNeurons-1)][random.randint(0, c.numMotorNeurons-1)] = random.random()*2 - 1

    def Create_Brain(self):
        pyrosim.Start_NeuralNetwork(f"brain{self.myID}.nndf")
        
        pyrosim.Send_Sensor_Neuron(name = 0, linkName = "Torso")     
        # pyrosim.Send_Sensor_Neuron(name = 1, linkName = "BackLeg")
        # pyrosim.Send_Sensor_Neuron(name = 2, linkName = "FrontLeg")
        # pyrosim.Send_Sensor_Neuron(name = 3, linkName = "LeftLeg")
        # pyrosim.Send_Sensor_Neuron(name = 4, linkName = "RightLeg")
        pyrosim.Send_Sensor_Neuron(name = 1, linkName = "FrontLowerLeg")
        pyrosim.Send_Sensor_Neuron(name = 2, linkName = "BackLowerLeg")
        pyrosim.Send_Sensor_Neuron(name = 3, linkName = "LeftLowerLeg")
        pyrosim.Send_Sensor_Neuron(name = 4, linkName = "RightLowerLeg")
        
        # pyrosim.Send_Motor_Neuron(name = 9, jointName = "Torso_BackLeg")
        # pyrosim.Send_Motor_Neuron(name = 10, jointName = "Torso_FrontLeg")
        # pyrosim.Send_Motor_Neuron(name = 11, jointName = "Torso_LeftLeg")
        # pyrosim.Send_Motor_Neuron(name = 12, jointName = "Torso_RightLeg")
        # pyrosim.Send_Motor_Neuron(name = 13, jointName = "FrontLeg_FrontLowerLeg")
        # pyrosim.Send_Motor_Neuron(name = 14, jointName = "BackLeg_BackLowerLeg")
        # pyrosim.Send_Motor_Neuron(name = 15, jointName = "LeftLeg_LeftLowerLeg")
        # pyrosim.Send_Motor_Neuron(name = 16, jointName = "RightLeg_RightLowerLeg")

        pyrosim.Send_Motor_Neuron(name = 5, jointName = "Torso_BackLeg")
        pyrosim.Send_Motor_Neuron(name = 6, jointName = "Torso_FrontLeg")
        pyrosim.Send_Motor_Neuron(name = 7, jointName = "Torso_LeftLeg")
        pyrosim.Send_Motor_Neuron(name = 8, jointName = "Torso_RightLeg")
        pyrosim.Send_Motor_Neuron(name = 9, jointName = "FrontLeg_FrontLowerLeg")
        pyrosim.Send_Motor_Neuron(name = 10, jointName = "BackLeg_BackLowerLeg")
        pyrosim.Send_Motor_Neuron(name = 11, jointName = "LeftLeg_LeftLowerLeg")
        pyrosim.Send_Motor_Neuron(name = 12, jointName = "RightLeg_RightLowerLeg")
    
        for currentRow in range(c.numSensorNeurons):
            for currentCol in range(c.numMotorNeurons):
                pyrosim.Send_Synapse(sourceNeuronName = currentRow, 
                                     targetNeuronName = currentCol + c.numSensorNeurons, 
                                     weight = self.weights[currentRow][currentCol])
    
        pyrosim.End()

def Create_World():
    pyrosim.Start_SDF("world.sdf")
    pyrosim.Send_Cube(name="Box", pos=[-5, 5, 0.5] , size=[1,1,1])
    pyrosim.End()   

def Create_Body():
    pyrosim.Start_URDF("body.urdf")
    pyrosim.Send_Cube(name="Torso", pos=[0, 0, 1], size=[1,1,1])
    
    pyrosim.Send_Joint(name="Torso_BackLeg", parent="Torso", child="BackLeg", type="revolute", position=[0,-0.5,1], jointAxis="1 0 0")
    pyrosim.Send_Cube(name="BackLeg", pos=[0, -0.5, 0] , size=[0.2,1,0.2])
    
    pyrosim.Send_Joint(name= "Torso_FrontLeg", parent="Torso", child="FrontLeg", type="revolute", position=[0,0.5,1], jointAxis="1 0 0")
    pyrosim.Send_Cube(name="FrontLeg", pos=[0, 0.5, 0], size=[0.2,1,0.2])
    
    pyrosim.Send_Joint(name="Torso_LeftLeg", parent="Torso", child="LeftLeg", type="revolute", position=[-0.5,0,1], jointAxis="0 1 0")
    pyrosim.Send_Cube(name="LeftLeg", pos=[-0.5, 0, 0], size=[1,0.2,0.2])
    
    pyrosim.Send_Joint(name="Torso_RightLeg", parent="Torso", child="RightLeg", type="revolute", position=[0.5,0,1], jointAxis="0 1 0")
    pyrosim.Send_Cube(name="RightLeg", pos=[0.5, 0, 0], size=[1,0.2,0.2])

    pyrosim.Send_Joint(name="FrontLeg_FrontLowerLeg", parent="FrontLeg", child="FrontLowerLeg", type="revolute", position=[0,1,0], jointAxis="1 0 0")
    pyrosim.Send_Cube(name="FrontLowerLeg", pos=[0, 0, -0.5], size=[0.2,0.2,1])

    pyrosim.Send_Joint(name="BackLeg_BackLowerLeg", parent="BackLeg", child="BackLowerLeg", type="revolute", position=[0,-1,0], jointAxis="1 0 0")
    pyrosim.Send_Cube(name="BackLowerLeg", pos=[0, 0, -0.5], size=[0.2,0.2,1])

    pyrosim.Send_Joint(name="LeftLeg_LeftLowerLeg", parent="LeftLeg", child="LeftLowerLeg", type="revolute", position=[-1,0,0], jointAxis="0 1 0")
    pyrosim.Send_Cube(name="LeftLowerLeg", pos=[0, 0, -0.5], size=[0.2,0.2,1])

    pyrosim.Send_Joint(name="RightLeg_RightLowerLeg", parent="RightLeg", child="RightLowerLeg", type="revolute", position=[1,0,0], jointAxis="0 1 0")
    pyrosim.Send_Cube(name="RightLowerLeg", pos=[0, 0, -0.5], size=[0.2,0.2,1])
    
    pyrosim.End()
    
