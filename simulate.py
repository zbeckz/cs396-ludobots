import pybullet as p
import pybullet_data
import time

# setup
physicsClient = p.connect(p.GUI)
p.setAdditionalSearchPath(pybullet_data.getDataPath())

# load world
p.setGravity(0,0,-9.8)
planeId = p.loadURDF("plane.urdf")
robotId = p.loadURDF("body.urdf")
p.loadSDF("world.sdf")


# simulate the world
for i in range(10000):
    print(i)    
    p.stepSimulation()
    time.sleep(1/60)

p.disconnect()