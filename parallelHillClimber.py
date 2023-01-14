from solution import SOLUTION
import constants as c
import copy
import os

class PARALLEL_HILL_CLIMBER:

    def __init__(self):
        os.system("del brain*.nndf")
        os.system("del fitness*.txt")
        self.nextAvailableID = 0
        self.parents = {}
        for i in range(c.populationSize):
            self.parents[i] = SOLUTION(self.nextAvailableID)
            self.nextAvailableID += 1 

    def Evolve(self):
        self.Evaluate(self.parents)
        for currentGeneration in range(c.numberOfGenerations):
           self.Evolve_For_One_Generation()

    def Evolve_For_One_Generation(self):
        self.Spawn()
        self.Mutate()
        self.Evaluate(self.children)
        self.Print()
        self.Select()

    def Evaluate(self, solutions):
        for sol in solutions.values():
            sol.Start_Simulation("DIRECT")
        for sol in solutions.values():
            sol.Wait_For_Simulation_To_End()

    def Spawn(self):
        self.children = {}
        for key in self.parents.keys():
            self.children[key] = copy.deepcopy(self.parents[key])
            self.children[key].Set_ID(self.nextAvailableID)
            self.nextAvailableID += 1

    def Mutate(self):
        for child in self.children.values():
            child.Mutate()

    def Select(self):
        for key in self.parents.keys(): 
            if self.parents[key].fitness > self.children[key].fitness:
                self.parents[key] = self.children[key]

    def Show_Best(self):
        best = self.parents[0]
        for parent in self.parents.values():
            if parent.fitness < best.fitness:
                best = parent
        best.Start_Simulation("GUI")

    def Print(self):
        for key in self.parents.keys():
            print(f'\nParent: {self.parents[key].fitness}, Child: {self.children[key].fitness}')
        print('\n------------------------------------')
