from simulation import SIMULATION
import sys
import pyrosim.pyrosim as pyrosim
import solution

directOrGUI = sys.argv[1]
solutionID = sys.argv[2]
simulation = SIMULATION(directOrGUI, solutionID)
simulation.Run()