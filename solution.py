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

        # sensor neurons for 4 legs that start from middle of torso
        pyrosim.Send_Sensor_Neuron(name = 1, linkName = "FrontLowerLeg")
        pyrosim.Send_Sensor_Neuron(name = 2, linkName = "BackLowerLeg")
        pyrosim.Send_Sensor_Neuron(name = 3, linkName = "LeftLowerLeg")
        pyrosim.Send_Sensor_Neuron(name = 4, linkName = "RightLowerLeg")
        
        # sensor neurons for 4 corner legs
        pyrosim.Send_Sensor_Neuron(name = 5, linkName = "FrontRightLowerLeg")
        pyrosim.Send_Sensor_Neuron(name = 6, linkName = "FrontLeftLowerLeg")
        pyrosim.Send_Sensor_Neuron(name = 7, linkName = "BackRightLowerLeg")
        pyrosim.Send_Sensor_Neuron(name = 8, linkName = "BackLeftLowerLeg")

        # motor neurons for middle legs
        pyrosim.Send_Motor_Neuron(name = 9, jointName = "Torso_BackLeg")
        pyrosim.Send_Motor_Neuron(name = 10, jointName = "Torso_FrontLeg")
        pyrosim.Send_Motor_Neuron(name = 11, jointName = "Torso_LeftLeg")
        pyrosim.Send_Motor_Neuron(name = 12, jointName = "Torso_RightLeg")
        pyrosim.Send_Motor_Neuron(name = 13, jointName = "FrontLeg_FrontLowerLeg")
        pyrosim.Send_Motor_Neuron(name = 14, jointName = "BackLeg_BackLowerLeg")
        pyrosim.Send_Motor_Neuron(name = 15, jointName = "LeftLeg_LeftLowerLeg")
        pyrosim.Send_Motor_Neuron(name = 16, jointName = "RightLeg_RightLowerLeg")

        # motor neurons for corner legs
        pyrosim.Send_Motor_Neuron(name = 17, jointName = "Torso_FrontRightLeg")
        pyrosim.Send_Motor_Neuron(name = 18, jointName = "Torso_FrontLeftLeg")
        pyrosim.Send_Motor_Neuron(name = 19, jointName = "Torso_BackRightLeg")
        pyrosim.Send_Motor_Neuron(name = 20, jointName = "Torso_BackLeftLeg")
        pyrosim.Send_Motor_Neuron(name = 21, jointName = "FrontRightLeg_FrontRightLowerLeg")
        pyrosim.Send_Motor_Neuron(name = 22, jointName = "FrontLeftLeg_FrontLeftLowerLeg")
        pyrosim.Send_Motor_Neuron(name = 23, jointName = "BackRightLeg_BackRightLowerLeg")
        pyrosim.Send_Motor_Neuron(name = 24, jointName = "BackLeftLeg_BackLeftLowerLeg")
    
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
    
    # 4 legs that start from middle of torso
    pyrosim.Send_Joint(name="Torso_BackLeg", parent="Torso", child="BackLeg", type="revolute", position=[0,-0.5,1], jointAxis="1 0 0")
    pyrosim.Send_Cube(name="BackLeg", pos=[0, -0.5, 0] , size=[0.2,1,0.2]) 
    pyrosim.Send_Joint(name= "Torso_FrontLeg", parent="Torso", child="FrontLeg", type="revolute", position=[0,0.5,1], jointAxis="1 0 0")
    pyrosim.Send_Cube(name="FrontLeg", pos=[0, 0.5, 0], size=[0.2,1,0.2])
    pyrosim.Send_Joint(name="Torso_LeftLeg", parent="Torso", child="LeftLeg", type="revolute", position=[-0.5,0,1], jointAxis="0 1 0")
    pyrosim.Send_Cube(name="LeftLeg", pos=[-0.5, 0, 0], size=[1,0.2,0.2])
    pyrosim.Send_Joint(name="Torso_RightLeg", parent="Torso", child="RightLeg", type="revolute", position=[0.5,0,1], jointAxis="0 1 0")
    pyrosim.Send_Cube(name="RightLeg", pos=[0.5, 0, 0], size=[1,0.2,0.2])

    # lower portions of the above 4 legs
    pyrosim.Send_Joint(name="FrontLeg_FrontLowerLeg", parent="FrontLeg", child="FrontLowerLeg", type="revolute", position=[0,1,0], jointAxis="1 0 0")
    pyrosim.Send_Cube(name="FrontLowerLeg", pos=[0, 0, -0.5], size=[0.2,0.2,1])
    pyrosim.Send_Joint(name="BackLeg_BackLowerLeg", parent="BackLeg", child="BackLowerLeg", type="revolute", position=[0,-1,0], jointAxis="1 0 0")
    pyrosim.Send_Cube(name="BackLowerLeg", pos=[0, 0, -0.5], size=[0.2,0.2,1])
    pyrosim.Send_Joint(name="LeftLeg_LeftLowerLeg", parent="LeftLeg", child="LeftLowerLeg", type="revolute", position=[-1,0,0], jointAxis="0 1 0")
    pyrosim.Send_Cube(name="LeftLowerLeg", pos=[0, 0, -0.5], size=[0.2,0.2,1])
    pyrosim.Send_Joint(name="RightLeg_RightLowerLeg", parent="RightLeg", child="RightLowerLeg", type="revolute", position=[1,0,0], jointAxis="0 1 0")
    pyrosim.Send_Cube(name="RightLowerLeg", pos=[0, 0, -0.5], size=[0.2,0.2,1])

    # 4 legs that start from corner of torso
    d = 0.5 / np.sqrt(2)
    pyrosim.Send_Joint(name="Torso_FrontRightLeg", parent="Torso", child="FrontRightLeg", type="revolute", position=[0.5,0.5,1], jointAxis="-1 1 0")
    pyrosim.Send_Cube(name="FrontRightLeg", pos=[d, d, 0], size=[1,0.2,0.2], rpy=f"0 0 {np.pi/4}") 
    pyrosim.Send_Joint(name= "Torso_FrontLeftLeg", parent="Torso", child="FrontLeftLeg", type="revolute", position=[-0.5,0.5,1], jointAxis="1 1 0")
    pyrosim.Send_Cube(name="FrontLeftLeg", pos=[-d, d, 0], size=[1,0.2,0.2], rpy=f"0 0 {-np.pi/4}")
    pyrosim.Send_Joint(name="Torso_BackRightLeg", parent="Torso", child="BackRightLeg", type="revolute", position=[0.5,-0.5,1], jointAxis="1 1 0")
    pyrosim.Send_Cube(name="BackRightLeg", pos=[d, -d, 0], size=[1,0.2,0.2], rpy=f"0 0 {-np.pi/4}")
    pyrosim.Send_Joint(name="Torso_BackLeftLeg", parent="Torso", child="BackLeftLeg", type="revolute", position=[-0.5,-0.5,1], jointAxis="-1 1 0")
    pyrosim.Send_Cube(name="BackLeftLeg", pos=[-d, -d, 0], size=[1,0.2,0.2], rpy=f"0 0 {np.pi/4}")

    # lower portions of the above 4 legs
    pyrosim.Send_Joint(name="FrontRightLeg_FrontRightLowerLeg", parent="FrontRightLeg", child="FrontRightLowerLeg", type="revolute", position=[2*d,2*d,0], jointAxis="-1 1 0")
    pyrosim.Send_Cube(name="FrontRightLowerLeg", pos=[0, 0, -0.5], size=[0.2,0.2,1])
    pyrosim.Send_Joint(name="FrontLeftLeg_FrontLeftLowerLeg", parent="FrontLeftLeg", child="FrontLeftLowerLeg", type="revolute", position=[-2*d,2*d,0], jointAxis="1 1 0")
    pyrosim.Send_Cube(name="FrontLeftLowerLeg", pos=[0, 0, -0.5], size=[0.2,0.2,1])
    pyrosim.Send_Joint(name="BackRightLeg_BackRightLowerLeg", parent="BackRightLeg", child="BackRightLowerLeg", type="revolute", position=[2*d,-2*d,0], jointAxis="1 1 0")
    pyrosim.Send_Cube(name="BackRightLowerLeg", pos=[0, 0, -0.5], size=[0.2,0.2,1])
    pyrosim.Send_Joint(name="BackLeftLeg_BackLeftLowerLeg", parent="BackLeftLeg", child="BackLeftLowerLeg", type="revolute", position=[-2*d,-2*d,0], jointAxis="-1 1 0")
    pyrosim.Send_Cube(name="BackLeftLowerLeg", pos=[0, 0, -0.5], size=[0.2,0.2,1])
    
    pyrosim.End()
    
