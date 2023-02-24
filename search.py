from parallelHillClimber import PARALLEL_HILL_CLIMBER
import constants as c
import sys
import random

c.numberOfGenerations = int(sys.argv[2])
c.populationSize = int(sys.argv[1])
if len(sys.argv) == 4:
    random.seed(int(sys.argv[3]))
    c.seed = int(sys.argv[3])
else:
    c.seed = random.randint(2222, 22222)
    random.seed(c.seed)
phc = PARALLEL_HILL_CLIMBER()
phc.Evolve()
phc.Show_Best()