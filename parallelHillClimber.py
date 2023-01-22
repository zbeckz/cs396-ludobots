from solution import SOLUTION
import constants as c
import copy
import os

class PARALLEL_HILL_CLIMBER:

    def __init__(self):
        # delete uneccesary files leftover by previous simulations
        os.system("del brain*.nndf")
        os.system("del fitness*.txt")

        # create random parents to evolve
        self.nextAvailableID = 0
        self.parents = {}
        for i in range(c.populationSize):
            self.parents[i] = SOLUTION(self.nextAvailableID)
            self.nextAvailableID += 1 

    # evaluate the parents, then evolve for all generations
    def Evolve(self):
        self.Evaluate(self.parents)
        for currentGeneration in range(c.numberOfGenerations):
           self.Evolve_For_One_Generation(currentGeneration)

    # pretty self explanatory - check the called methods' descriptions
    def Evolve_For_One_Generation(self, gen):
        self.Spawn()
        self.Mutate()
        self.Evaluate(self.children)
        self.Print(gen)
        self.Select()

    # simulate all given solutions in parallel, gathering fitness data internally
    def Evaluate(self, solutions):
        for sol in solutions.values():
            sol.Start_Simulation("DIRECT")
        for sol in solutions.values():
            sol.Wait_For_Simulation_To_End()

    # for all parents, copy a child
    def Spawn(self):
        self.children = {}
        for key in self.parents.keys():
            self.children[key] = copy.deepcopy(self.parents[key])
            self.children[key].Set_ID(self.nextAvailableID)
            self.nextAvailableID += 1

    # randomly mutate every child
    def Mutate(self):
        for child in self.children.values():
            child.Mutate()

    # if the child is better than parent, replace it
    def Select(self):
        for key in self.parents.keys(): 
            if self.children[key].fitness > self.parents[key].fitness:
                self.parents[key] = self.children[key]

    # find the best parent, simulate it with the GUI
    def Show_Best(self):
        best = self.parents[0]
        for parent in self.parents.values():
            if parent.fitness > best.fitness:
                best = parent
        best.Start_Simulation("GUI")

    def Print(self, gen):
        print(f'\n---------------GEN {gen+1}---------------')
        for key in self.parents.keys():
            print("Parent: {:.2f}, Child: {:.2f}".format(self.parents[key].fitness, self.children[key].fitness))
        print('------------------------------------')
