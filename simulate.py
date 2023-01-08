import pybullet as p
import pybullet_data
import time
import pyrosim.pyrosim as pyrosim
import numpy as np
import random

# setup
physicsClient = p.connect(p.GUI)
p.setAdditionalSearchPath(pybullet_data.getDataPath())

forceMax = 500
iterations = 1000

backLegSensorValues = np.zeros(iterations)
frontLegSensorValues = np.zeros(iterations)

backAmplitude = np.pi/8
backFrequency = 10
backPhaseOffset = 0

frontAmplitude = np.pi/8
frontFrequency = 10
frontPhaseOffset = np.pi/4

myRange = np.arange(0, 2*np.pi, 2*np.pi/iterations)
backTargetAngles = backAmplitude * np.sin(backFrequency * myRange + backPhaseOffset)
frontTargetAngles = frontAmplitude * np.sin(frontFrequency * myRange + frontPhaseOffset)
# np.save("data/backTargetAngles", backTargetAngles)
# np.save("data/frontTargetAngles", frontTargetAngles)
# exit()

# load world
p.setGravity(0,0,-9.8)
planeId = p.loadURDF("plane.urdf")
robotId = p.loadURDF("body.urdf")
p.loadSDF("world.sdf")
pyrosim.Prepare_To_Simulate(robotId)


# simulate the world
for i in range(iterations): 
    p.stepSimulation()
    backLegSensorValues[i] = pyrosim.Get_Touch_Sensor_Value_For_Link("BackLeg")
    frontLegSensorValues[i] = pyrosim.Get_Touch_Sensor_Value_For_Link("FrontLeg")
    
    pyrosim.Set_Motor_For_Joint(bodyIndex=robotId, 
                                jointName="Torso_BackLeg", 
                                controlMode=p.POSITION_CONTROL, 
                                targetPosition=backTargetAngles[i], 
                                maxForce=forceMax)

    pyrosim.Set_Motor_For_Joint(bodyIndex=robotId, 
                                jointName="Torso_FrontLeg", 
                                controlMode=p.POSITION_CONTROL, 
                                targetPosition=frontTargetAngles[i], 
                                maxForce=forceMax)
    
    time.sleep(1/60)

p.disconnect()
np.save("data/backLegSensorValues", backLegSensorValues)
np.save("data/frontLegSensorValues", frontLegSensorValues)