from simulation import SIMULATION
import sys
import pyrosim.pyrosim as pyrosim
import solution

solution.Create_Body()
solution.Create_World()
directOrGUI = sys.argv[1]
solutionID = sys.argv[2]
simulation = SIMULATION(directOrGUI, solutionID)
simulation.Run()
simulation.Get_Fitness(solutionID)