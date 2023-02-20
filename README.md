# CS396 - Assignment 7
This code base was built For CS396 at Northwestern University. Its foundation was written by following the MOOC found on the subreddit r/ludobots, which includes forking the PryoSim repository https://github.com/jbongard/pyrosim.git. The physics is simulated using PyBullet

VIDEO: 
https://youtu.be/lAxipjH3Vbc

INSTRUCTIONS: 
Run python search.py to randomly create and simulate a body and brain. Run it mulitple times to see the variety in possible creatures

BODY DESCRIPTION:
In the following description, refer to this diagram for cube numbers

![image text](https://imgur.com/a/70W5W4A)

Links are created using a custom made function. This function takes in a position for the joint that will connect this new link to previous link, as well as a direction that the new link is being placed in. Imagine we create link 3 using this function - it will be given a position for a joint that is placed in the middle of the right face of link 2, and told the direction is to the right. 

After creating the link, the function uses probabilities defined earlier in the code to determine if links are placed in positions 4, 5, 6, 7, or 8. It is possible for none of these to be placed, or all of them. The function recursively calls itself with the correct joint position and direction depending on which of the positions it placing the next link in, and it cannot place one in the direction of the previous link so they aren't placed in the same spot. 

As of right now, the probabilities are such that there is a 90% chance of a new link being placed in the same direction that this link was created in, and the other directions each have a 10% chance of occuring. This is a design choice to create longer limbs while still allowing for some branching / turning.

