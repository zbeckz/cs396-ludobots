import pyrosim.pyrosim as pyrosim

pyrosim.Start_SDF("boxes.sdf")

# first box
x = 0
y = 0
z = 0.5
length = 1
width = 1
height = 1
pyrosim.Send_Cube(name="Box", pos=[x,y,z] , size=[length,width,height])

# second box
x = 1
y = 0
z = 1.5
pyrosim.Send_Cube(name="Box2", pos=[x,y,z] , size=[length,width,height])

pyrosim.End()