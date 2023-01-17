import os
from parallelHillClimber import PARALLEL_HILL_CLIMBER
import constants as c
import sys

c.populationSize = int(sys.argv[1])
c.numberOfGenerations = int(sys.argv[2])
phc = PARALLEL_HILL_CLIMBER()
phc.Evolve()
phc.Show_Best()