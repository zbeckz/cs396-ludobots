import pybullet as p
import pybullet_data
import time
import pyrosim.pyrosim as pyrosim
import numpy as np
import random
import constants as c

# setup
physicsClient = p.connect(p.GUI)
p.setAdditionalSearchPath(pybullet_data.getDataPath())

backLegSensorValues = np.zeros(c.iterations)
frontLegSensorValues = np.zeros(c.iterations)

myRange = np.arange(0, 2*np.pi, 2*np.pi/c.iterations)
backTargetAngles = c.backAmplitude * np.sin(c.backFrequency * myRange + c.backPhaseOffset)
frontTargetAngles = c.frontAmplitude * np.sin(c.frontFrequency * myRange + c.frontPhaseOffset)
# np.save("data/backTargetAngles", backTargetAngles)
# np.save("data/frontTargetAngles", frontTargetAngles)
# exit()

# load world
p.setGravity(0,0,c.gravity)
planeId = p.loadURDF("plane.urdf")
robotId = p.loadURDF("body.urdf")
p.loadSDF("world.sdf")
pyrosim.Prepare_To_Simulate(robotId)


# simulate the world
for i in range(c.iterations): 
    p.stepSimulation()
    backLegSensorValues[i] = pyrosim.Get_Touch_Sensor_Value_For_Link("BackLeg")
    frontLegSensorValues[i] = pyrosim.Get_Touch_Sensor_Value_For_Link("FrontLeg")
    
    pyrosim.Set_Motor_For_Joint(bodyIndex=robotId, 
                                jointName="Torso_BackLeg", 
                                controlMode=p.POSITION_CONTROL, 
                                targetPosition=backTargetAngles[i], 
                                maxForce=c.forceMax)

    pyrosim.Set_Motor_For_Joint(bodyIndex=robotId, 
                                jointName="Torso_FrontLeg", 
                                controlMode=p.POSITION_CONTROL, 
                                targetPosition=frontTargetAngles[i], 
                                maxForce=c.forceMax)
    
    time.sleep(1/60)

p.disconnect()
np.save("data/backLegSensorValues", backLegSensorValues)
np.save("data/frontLegSensorValues", frontLegSensorValues)