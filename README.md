# CS396 - Final Project - Scientist Option
This code base was built For CS396 at Northwestern University. Its foundation was written by following the MOOC found on the subreddit r/ludobots, which includes forking the PryoSim repository https://github.com/jbongard/pyrosim.git. The physics is simulated using PyBullet. The fitness of a creature is determined by how far in the negative x direction (left and into the screen) it reaches by the end of the simulation. The goal of this assignment is the create and test a hypothesis regarding the evolution of these virtual creatures - this hypothesis and experiment can be found at the bottom of this page along with a short summary video.

### Body Generation

The inspiration for my creatures was to resemble centipedes. I decided 4 distinct types of links were necessary for this, which I called Torso, Body, Leg, and Foot links:

<img src="ReadmeImages/PhenotypeDiagram.jpg" width="50%" height="50%">

The algorithm I created for generating the above creature simplifies to this:

<img src="ReadmeImages/GenerationDiagram.jpg" width="50%" height="50%">

And once implemented produces a creature like this:

<img src="ReadmeImages/ExampleCreature.png" width="50%" height="50%">

The code has many parameters which can be changed to alter the creature generation. It is possible for there to be multiple leg links connected to each other, as with foot links. The size of each type of link can be modified along with how many torso links there should be, how many body links between each torso, how many links each leg has, and how many links each foot has. These parameters are randomly assigned in the constructor of *solution.py*

The algorithm utilizes recursion and variables that store how many of each type of link have been created thus far. There are individual functions for creating each type of link which may call themselves or the other functions depending on how far along the algorithm. Revolute joints are created between each adjacent link. Torso_Leg and Leg_Leg joints rotate around the x-axis. Leg_Foot and Foot_Foot joints rotate around the y axis. Torso_Torso, Torso_Body, and Body_Body joints rotate 
around the z-axis

### Body Evolution

Bodily evolution is simple. A random type of link is chosen to be mutated. One of the 4 parameters is chosen to be mutated (number, length, width, height). This parameter is changed by a random amount (float for size, integer for number), and there are checks in place to ensure nothing is 0 (except for body link number which cannot be negative)

### Brain Generation

The brain consists of sensor neurons in every bottom foot (colored green in the simulation) and motor neurons in every joint. Coding this part is straightforward - the complexity arises from the synaptic structure. A sensor neuron for a given foot is connected to every joint up the foot, through the leg, and within the foot and leg coming out of the same torso link. It will also be connected to the Torso_Body joints that connect its torso to the next torso link in either direction, a drawing of which can be seen below. This is done in code via math involving the parameters that determine the number of each type of link which can be found in *solution.py*'. Every synapse is given a random weight between -1 and 1

<img src="ReadmeImages/SynapseStructure.jpg" width="50%" height="50%">

### Brain Evolution

The brain evolves by picking a random synapse and changing its weight to a random number. If there are new links in the body's mutation, new synapses are created accordingly with random weights. If there were links removed in the body's mutation, those synapses are removed.

### Evolutionary Algorithm

I am using a parallel hill climber to perform evolution. Any number of creatures can be chosen to evolve for any number of generations. Each creature is randomly generated to start. For every generation, each creature creates a "child" creature that is identical to itself aside from 1 bodily mutation and 1 neurological mutation, as described in the evolution sections above. If the child performs better than its parent, it replaces the parent along that creature's lineage. Otherwise, the parent continues. All creatures undergo this process in parallel, generation by generation, and the fitness values are printed to the terminal, as seen below:

IMAGE TO BE PLACED HERE

### Hypothesis

My hypothesis was that bipedal creatures were able to achieve better fitness than quadrupedal creatures under my evolutionary conditons. This was inspired by my work done for assignment eight, as seen in the *assignmentEight* branch of this repository. It seemed to me that the creatures that ended up bipedal achieved better looking gaits. Perhaps this was due to having more simple bodies that allowed the brain to be more optimized, or perhaps this was due to my bias as a bipedal human. There's only one way to find out - run an experiment!

### Teaser

VIDEO TO BE PLACED HERE

### Summary

VIDEO TO BE PLACED HERE

### Executable

- Run "python search.py [numCreatures] [numGenerations] [numLegs] [seed]", where [seed] is optional and [numLegs] must be an even number
  -  "python search.py 5 20 4 12" would evolve 5 quadrupedal creatures in parallel for 20 generations with random seed 12
  -  "python search.py 10 100 2" would evolve 10 bipedal creatures in parallel for 100 generations, with a seed that is randomly generated
-  The fitness of the best creature in every generation will be output into a file named *numCreatures_numGenerations_numLegs_seed.txt* in a directory named *FitnessData*
-  The best creature of the first generation will be shown at the beginning, and the best creature of the final generation will be shown at the end

### Experimental Design

### Results

### Conclusion
