import pybullet as p
import pybullet_data
import time

# setup
physicsClient = p.connect(p.GUI)
p.setAdditionalSearchPath(pybullet_data.getDataPath())

# load world
p.setGravity(0,0,-9.8)                  # gravity
planeId = p.loadURDF("plane.urdf")      # floor
p.loadSDF("world.sdf")                  # world with just a box in it

# simulate the world
for i in range(10000):
    print(i)    
    p.stepSimulation()
    time.sleep(1/60)

p.disconnect()