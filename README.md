# cs396-ludobots
For CS396 at Northwestern University, using the MOOC found on the subreddit r/ludobots

GOALS:
1. The goal of my final project is to train a 4 legged robot to kick a ball as far away from it as possible. 
2. Initial robots typically move in a random direction or stand still, not interacting with the ball whatsoever. After undergoing 20 generations of evolution, with 10 robots hill climbing in parallel, the best ones would often move towards the ball, kick it, then either stand still or move away from the ball. This takes advantage of the fitness function that measures the maximum distance between the robot and the ball. A video example of this can be seen here: https://youtu.be/m5hiuh3CM-4

INSTRUCTIONS:
1. To replicate my results, use the "search.py" file. 
2. Run "python search.py" to run evolution with a population size of 10 for 20 generations
3. If you want to customize those numbers, run "python search.py {populationSize} {generations}". For example, do "python search.py 1 1" to see a single randomly generated robot that had 1 chance to evolve. This was the command I used to show a random robot in the above example.