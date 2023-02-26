# CS396 - Assignment 8
This code base was built For CS396 at Northwestern University. Its foundation was written by following the MOOC found on the subreddit r/ludobots, which includes forking the PryoSim repository https://github.com/jbongard/pyrosim.git. The physics is simulated using PyBullet. The goal is for creatures to evolve so that they move in the negative x direction (backwards and left into the screen)

**VIDEO:**

https://youtu.be/YCHTICpxCiI

**INSTRUCTIONS FOR EVOLUTION:** 

Run "python search.py [*p*] [*g*] [*s*]" 

Replace the words in brackets with numbers of your choice to randomly generate *p* creatures and evolve them in parallel for *g* generations. *s* is optional and represents a seed for the random number generator so that results can be reproduced - if no argument is included for *s* it will be randomly generated for you.

**INSTRUCTIONS FOR ANALYSIS:**

After running search.py the evolution, a file will have been created into a directory *FitnessData*. The file will have name "*p*_*g*_*s*.txt" and will contain be the best fitness for each generation on a new line.

Run "python analyze.py" to generate fitness curves for every file in *FitnessData*, which are all plotted on the same figure. This figure will be saved into the *FitnessCurves* directory as a png file. These figures are generated using matplotlib. Here is an example of one such curve:

<img src="FitnessCurves/Curve1.png" width="50%" height="50%">

**BODY GENERATION:**

The inspiration for my creatures was to resemble centipedes. I decided 4 distinct types of links were necessary for this, which I called Torso, Body, Leg, and Foot links:

<img src="ReadmeImages/PhenotypeDiagram.jpg" width="50%" height="50%">

The algorithm I created for generating the above creature simplifies to this:

<img src="ReadmeImages/GenerationDiagram.jpg" width="50%" height="50%">

And once put in code creates a creature like this:



**BRAIN GENERATION:**

**BODY EVOLUTION:**

**BRAIN EVOLUTION:**
