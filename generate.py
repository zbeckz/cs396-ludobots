import pyrosim.pyrosim as pyrosim

# makes a tower of 10 boxes, with each higher box being 90% the size of the one below it, with base at (x, y, 0)
def makeTower(x, y):
    for i in range(10):
        z = 0.5 + i             # each block placed on top of one before it
        length = 1 * 0.9**i     # each block 90% size of one before it
        width = 1 * 0.9**i
        height = 1 * 0.9**i
        pyrosim.Send_Cube(name="Box " + str(i+1), pos=[x,y,z] , size=[length,width,height])

def main():
    pyrosim.Start_SDF("boxes.sdf")

    # generate a 5 by 5 grid of towers
    for i in range(-2, 3):
        for j in range(-2, 3):
            makeTower(i, j)

    pyrosim.End()    

if __name__ == "__main__":
    main()
