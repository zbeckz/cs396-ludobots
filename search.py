import os
from parallelHillClimber import PARALLEL_HILL_CLIMBER
import constants as c
import sys

args = sys.argv
if len(args) != 1: 
    c.populationSize = int(sys.argv[1])
    c.numberOfGenerations = int(sys.argv[2])
phc = PARALLEL_HILL_CLIMBER()
phc.Evolve()
phc.Show_Best()