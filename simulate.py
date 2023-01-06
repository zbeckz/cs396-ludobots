import pybullet as p
import time

physicsClient = p.connect(p.GUI)

# load box into the world
p.loadSDF("box.sdf")

# show the world for some time
for i in range(10000):
    print(i)    
    p.stepSimulation()
    time.sleep(1/60)

p.disconnect()