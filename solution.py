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
        pyrosim.End()

def Create_World():
    pyrosim.Start_SDF("world.sdf")
    pyrosim.End()

def Create_Body():
    pyrosim.Start_URDF("body.urdf")
    pyrosim.End()
    
