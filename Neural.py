
import random
import numpy as np
import copy
import operator
import time
import datetime

class Network():

    def __init__(self, i, h, o):
        self.iNodes = i #input nodes
        self.hNodes = h #hidden nodes
        self.oNodes = o #output nodes

        self.iWeights = 2 * np.random.random((h, i + 1)) - 1 #incldudes bias
        self.hWeights = 2 * np.random.random((h, h + 1)) - 1 # hidden level 1
        self.oWeights = 2 * np.random.random((o, h + 1)) - 1 # hidden level 2

    def mutate(self, matrix, rate):
        for i, r in enumerate(matrix):
            for j, c in enumerate(r):
                # if selected to mutate
                if random.uniform(0, 1) < rate:
                    matrix[i][j] += matrix[i][j] * np.random.normal(0,0.25)
                    if matrix[i][j] > 1:
                        matrix[i][j] = 1
                    elif matrix[i][j] < -1:
                        matrix[i][j] = -1

    def mutateAll(self, rate):
        self.mutate(self.iWeights, rate)
        self.mutate(self.hWeights, rate)
        self.mutate(self.oWeights, rate)

    def sigmoid(self, x):
        return 1 / (1 + np.exp(-x))

    # pass through sigmoidal activation function
    def activate(self, matrix):
        for i, r in enumerate(matrix):
            for j, c in enumerate(r):
                matrix[i][j] = self.sigmoid(matrix[i][j])
        return matrix

    # turns the matrix into a column then adds one to the bottom (for dot product)
    def addBias(self, m, sz):
        n = np.array(m).flatten()
        n = np.append(n, [1]).reshape(sz + 1, 1)
        return n

    def output(self, matrix):
        # ----------- hidden layer one  ----------
        #add 1 to the bottom to account for bias
        input = self.addBias(matrix, self.iNodes)
        #dot product
        hiddenInputs = np.dot(self.iWeights, input)
        #activate
        hiddenOutputs = self.activate(hiddenInputs)

        # ------------ hidden layer two ------------
        #add 1 to the bottom to account for bias
        hiddenOutputs = self.addBias(hiddenOutputs, self.hNodes)
        hiddenInputs2 =  np.dot(self.hWeights, hiddenOutputs)
        hiddenOutputs2 = self.activate(hiddenInputs2)

        # ------------ Calculate Output ------------
        #add 1 to the bottom to account for bias
        hiddenOutputs2 = self.addBias(hiddenOutputs2, self.hNodes)
        outputInputs = np.dot(self.oWeights, hiddenOutputs2)
        outputs = self.activate(outputInputs)

        #return index of highest result
        highest = max(outputs.flatten())
        for i, j in enumerate(outputs.flatten()):
            if j == highest:
                #print("move:", outputs)
                return i


class Individual():
    def __init__(self):
        self.brain = Network(200,25,4)
        self.score = 0
        self.level = 1
        self.fitness = 0
        self.timeAlive = 0
        self.data = []

    def setFitness(self):
        self.fitness = self.score + self.timeAlive

    def clone(self):
        a = Individual()
        a.brain = copy.deepcopy(self.brain)
        return a

    def breed(self, partner):
        child = Individual()
        child.brain.iWeights = self.meiosis(self.brain.iWeights, partner.brain.iWeights)
        child.brain.hWeights = self.meiosis(self.brain.hWeights, partner.brain.hWeights)
        child.brain.oWeights = self.meiosis(self.brain.oWeights, partner.brain.oWeights)
        return child

    def meiosis(self,father, mother):
        child = copy.deepcopy(father)
        m = copy.deepcopy(mother)

        #half from father, half from mother
        for i, r in enumerate(m):
            for j, c in enumerate(r):
                if random.uniform(0, 1) > 0.5:
                    child[i][j] = c
        return child

class Population():
    def __init__(self, sz):
        self.size = sz
        self.gen = 1
        self.globalBest = 0.0 #global best score
        self.currentBest = 0.0 #current best score
        self.keep = 10
        self.data = np.random.randint(0, 7, size=1000)
        self.elite = 3

        self.pop = []
        for _ in range(sz):
            self.pop.append(Individual())
        self.globalBestIndividual = self.pop[0].clone() #copy of global best

    def save(self):
        ts = time.time()
        st = datetime.datetime.fromtimestamp(ts).strftime('%Y-%m-%d %H:%M:%S') + " " + self.gen + " " + str(self.globalBest)
        np.savez(st, iWeights = self.globalBestIndividual.brain.iWeights, hWeights = self.globalBestIndividual.brain.hWeights,
                 oWeights = self.globalBestIndividual.brain.oWeights, data = self.globalBestIndividual.data)

    def setBest(self):
        # sort list based on fitness
        self.pop.sort(key=operator.attrgetter('fitness'), reverse= True)

        self.totalFitness = 0

        for i in range(self.size):
            self.totalFitness += self.pop[i].fitness

        self.currentBest = self.pop[0].fitness
        print("current best", self.currentBest, "global best", self.globalBest)
        if self.currentBest > self.globalBest:
            self.globalBestIndividual = self.pop[0].clone()
            self.globalBest = self.pop[0].fitness
            self.globalBestIndividual.data = copy.deepcopy(self.data)
            self.save()

    #create next generation of individuals
    def evolve(self):
        print("EVOLLLVE")
        self.gen += 1

        #copy best 3 without mutation
        # one buffer since the first individual always gets messed up due to computation time
        new = [] #Individual()
        for i in range(0, self.size):
            print(i)
            if i < self.elite:
                print ("keep, don't mutate")
                new.append(self.pop[i])
                continue # don't mutate
            elif i < self.keep:
                print("keep")
                new.append(self.pop[i]) #mutate though
            #keep some
            elif random.uniform(0, 1) > 0.90:
                print("keep")
                new.append(self.pop[i])
            #get random offspring for the rest
            else:
                #selecting parents using Roulette Sampling
                current = 0
                limA = random.randrange(self.totalFitness)
                limB = random.randrange(self.totalFitness)
                a = -1
                b = -1
                for j in range(self.size):
                    current += self.pop[j].fitness
                    if limA < current and a == -1:
                        a = j
                    if limB < current and b == -1:
                        b = j

                print("mate", a, "with", b)
                new.append(self.pop[a].breed(self.pop[b]))
            #MUTATE THEM!
            print("mutating!")
            new[i].brain.mutateAll(0.1)

        #get new data
        #self.data = np.random.randint(0, 7, size=1000)

        time.sleep(1)
        return new

