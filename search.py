from parallelHillClimber import PARALLEL_HILL_CLIMBER
import constants as c
import sys
import random

# run python search.py [popSize] [numGenerations] [numLegs] [seed] where seed is optional and numLegs must be an even number

c.numberOfGenerations = int(sys.argv[2])
c.populationSize = int(sys.argv[1])
numLegs = int(sys.argv[3])
if numLegs % 2 == 0:
    c.numTorso = int(sys.argv[3])/2
else:
    print("\nERROR: Please input an even number of legs\n")
    exit()
if len(sys.argv) == 5:
    random.seed(int(sys.argv[3]))
    c.seed = int(sys.argv[3])
else:
    c.seed = random.randint(2222, 22222)
    random.seed(c.seed)
phc = PARALLEL_HILL_CLIMBER()
phc.Evolve()
phc.Show_Best()