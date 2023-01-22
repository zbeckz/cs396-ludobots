import numpy as np
import pyrosim.pyrosim as pyrosim
import os
import random
import time
import constants as c

class SOLUTION:

    def __init__(self, id):
        self.myID = id
        if c.numHiddenNeurons == 0:
            self.weights = np.random.rand(c.numSensorNeurons, c.numMotorNeurons) * 2 - 1
        else:
            self.sensorToHiddenWeights = np.random.rand(c.numSensorNeurons, c.numHiddenNeurons) * 2 - 1
            self.hiddenToMotorWeights = np.random.rand(c.numHiddenNeurons, c.numMotorNeurons) * 2 - 1

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
        
        # torso sensor
        pyrosim.Send_Sensor_Neuron(name = 0, linkName = "Torso")

        counter = 1
        # create sensor neurons
        for i in range(c.numLegs):
            name = c.legNames[i]
            pyrosim.Send_Sensor_Neuron(name = counter, linkName = f"{c.legNames[i]}LowerLeg")
            counter += 1

        # create hidden neurons
        for i in range(c.numHiddenNeurons):
            pyrosim.Send_Hidden_Neuron(name = counter)
            counter += 1
            
        # create motor neurons
        for i in range(c.numLegs):
            pyrosim.Send_Motor_Neuron(name = counter, jointName = f"Torso_{c.legNames[i]}Leg") # torso to leg joints
            counter += 1
            pyrosim.Send_Motor_Neuron(name = counter, jointName = f"{c.legNames[i]}Leg_{c.legNames[i]}LowerLeg") # leg to lower leg joints
            counter += 1

        if c.numHiddenNeurons == 0:
            for currentRow in range(c.numSensorNeurons):
                for currentCol in range(c.numMotorNeurons):
                    pyrosim.Send_Synapse(sourceNeuronName=currentRow, targetNeuronName=currentCol + c.numSensorNeurons, weight=self.weights[currentRow][currentCol])
        else:
            # create synapses from every sensor to every hidden neuron
            for currentRow in range(c.numSensorNeurons):
                for currentCol in range(c.numHiddenNeurons):
                    pyrosim.Send_Synapse(sourceNeuronName = currentRow, targetNeuronName = currentCol + c.numSensorNeurons, weight = self.sensorToHiddenWeights[currentRow][currentCol])
        
            # create synapses from every hidden neuron to every motor neuron
            for currentRow in range(c.numHiddenNeurons):
                for currentCol in range(c.numMotorNeurons):
                    pyrosim.Send_Synapse(sourceNeuronName = currentRow + c.numSensorNeurons, targetNeuronName = currentCol + c.numSensorNeurons + c.numHiddenNeurons, weight = self.hiddenToMotorWeights[currentRow][currentCol])
        
        pyrosim.End()

def Create_World():
    pyrosim.Start_SDF("world.sdf")
    if c.fitness == "kickBall":
        pyrosim.Send_Sphere(name="KickBall", pos=c.kickBallStartingPosition , size=[0.5])
    if c.fitness == "target":
        pyrosim.Send_Sphere(name="KickBall", pos=c.kickBallStartingPosition , size=[0.5])
        pyrosim.Send_Sphere(name="targetBall", pos=c.targetBallStartingPosition , size=[0.5])
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

    # if its 8 legged
    if c.numLegs == 8:
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
    
