import Writer
import Parser
import sys
import random
import math
import numpy as np


# Experiment:

INIT_NODE = '0'
BETA = 0.990
INIT_TEMP = 100
OPT = 2
RANDOM = True
FILENAME = "AISearchfile048.txt"
SUCCESSOR = 'quad'


def main():

    distances = Parser.loadSearchFile(FILENAME)  # Distance matrix
    numNodes = len(distances)
    graph = Parser.createGraph(distances)

    if RANDOM:
        currentTour = random.sample(range(0, numNodes), numNodes)
        length = cost(currentTour, distances)
    else:
        currentTour, length = greedy(graph, numNodes)  # Create a tour

    for k in range(1, 5000000):  # k = iteration no.

        if SUCCESSOR == 'exp':
            t = scheduleExp(k)
        elif SUCCESSOR == 'log':
            t = scheduleLog(k)
        elif SUCCESSOR == 'lin':
            t = scheduleLin(k)
        elif SUCCESSOR == 'quad':
            t = scheduleQuad(k)

        if t <= 0.000001:  # Experiment
            return numNodes, currentTour, cost(currentTour, distances)

        if OPT == 2:
            nextTour = successor2opt(currentTour)
        else:
            nextTour = successor3opt(currentTour)

        delta = cost(currentTour, distances) - cost(nextTour, distances)

        if delta >= 0:
            currentTour = nextTour

        else:
            if random.random() < math.exp(delta / t):
                currentTour = nextTour

    return numNodes, currentTour, cost(currentTour, distances)
    # print tour, length
    # Writer.writeTourFile(FILENAME, numNodes, length, tour)

# T = 18000 for 40, 110000 for 80


def scheduleExp(k):  # BETA ~ 0.95
    return INIT_TEMP * math.pow(BETA, k)  # Experiment with this


def scheduleLog(k):  # BETA ~ 250 for 40, 2300 for 80
    return INIT_TEMP / (1 + BETA * math.log(1 + k))


def scheduleLin(k):  # BETA ~ 10 for 40, 66 for 80
    return INIT_TEMP / (1 + BETA * k)


def scheduleQuad(k):  # BETA ~ 0.05 for 40, 0.35 for 80
    return INIT_TEMP / (1 + BETA * math.pow(k, 2))


def scheduleLinN(k, n):
    return INIT_TEMP / (1 + BETA * math.pow(k, n))


def successor2opt(tour):
    newTour = tour[:]
    length = len(tour)
    a = random.randint(0, length)
    b = random.randint(0, length)

    while b == a:
        b = random.randint(0, length)

    if(abs(a - b) > 2):
        if(a < b):
            middle = tour[a:b]
            reverse = middle[::-1]
            newTour[a:b] = reverse
        else:
            middle = tour[b:a]
            reverse = middle[::-1]
            newTour[b:a] = reverse

    return newTour


def successor3opt(tour):
    newTour = tour[:]
    length = len(tour)
    a = random.randint(0, length - 1)
    b = random.randint(0, length - 1)
    c = random.randint(0, length - 1)

    while a == b or a == c or b == c:
        b = random.randint(0, length - 1)
        c = random.randint(0, length - 1)

    newTour[a], newTour[b], newTour[c] = newTour[b], newTour[c], newTour[a]
    # newTour[a], newTour[b], newTour[c] = newTour[c], newTour[a], newTour[b]
    # The other 3 opt result

    return newTour


def cost(tour, distances):  # how representing graph - implementation

    length = len(tour)
    cost = 0

    for i in range(length - 1):
        cost += distances[int(tour[i])][int(tour[i + 1])]

    cost += distances[int(tour[0])][int(tour[-1])]
    return cost


def greedy(graph, numNodes):
    unvisited = [str(i) for i in range(numNodes)]
    pTour = [INIT_NODE]  # Vary for experimentation
    unvisited.remove(INIT_NODE)
    minimum = sys.maxsize
    length = 0

    while len(unvisited) != 0:

        minimum = sys.maxsize

        for child in graph.get(pTour[-1]):  # For each child
            if child.name in unvisited:
                if child.dist < minimum:
                    minimum = child.dist
                    closest = child.name

        length += minimum

        pTour.append(closest)
        unvisited.remove(closest)

    nodes = graph.get(pTour[-1])

    for node in nodes:
        if node.name == pTour[0]:
            length += node.dist

    return pTour, length


if __name__ == '__main__':

    files = [535]
    successors = ['exp', 'log', 'lin', 'quad']

    bestTours = {}
    bestLengths = {}
    bestBetas = {}
    bestOpts = {}
    bestRands = {}
    bestSuccesses = {}

    for f in files:  # Loop through each file
        bestTour = []
        bestLength = sys.maxsize
        bestBeta = 0
        bestOpt = 2
        bestRand = True
        bestSuccess = 'exp'

        for i in range(f):  # Loop through each start node
            #for s in successors:  # Loop through each successor function
                betas = np.linspace(0.35, 0.55, 20, endpoint=False)
                for b in betas:  # Loop through each beta value
                    for k in range(2, 3):  # 2 or 3 opt
                        INIT_NODE = str(i)
                        BETA = b
                        OPT = k
                        RANDOM = False
                        #SUCCESSOR = s
                        if f < 100:
                            FILENAME = "AISearchfile0" + str(f) + ".txt"
                        else:
                            FILENAME = "AISearchfile" + str(f) + ".txt"
                        numNodes, tour, length = main()

                        if length < bestLength:
                            bestLength = length
                            bestTour = tour
                            bestBeta = b
                            bestOpt = k
                            bestRand = False
                            bestSuccess = SUCCESSOR

                            print bestLength
                            print bestTour
                            print bestBeta
                            print bestOpt
                            print bestRand
                            print bestSuccess

        betas = np.linspace(0.35, 0.55, 20, endpoint=False)
        for b in betas:  # Loop through each beta value
            #for s in successors:  # Loop through each successor function
                for k in range(2, 3):  # 2 or 3 opt
                    for l in range(5):  # Run 5 times on random
                        INIT_NODE = str(i)
                        BETA = b
                        OPT = k
                        RANDOM = True
                        #SUCCESSOR = s
                        numNodes, tour, length = main()

                        if length < bestLength:
                            bestLength = length
                            bestTour = tour
                            bestBeta = b
                            bestOpt = k
                            bestRand = True
                            bestSuccess = SUCCESSOR

                            print bestLength
                            print bestTour
                            print bestBeta
                            print bestOpt
                            print bestRand
                            print bestSuccess

        bestTours[f] = bestTour
        bestLengths[f] = bestLength
        bestBetas[f] = bestBeta
        bestOpts[f] = bestOpt
        bestRands[f] = bestRand
        bestSuccesses[f] = bestSuccess

        print bestTours
        print
        print bestLengths
        print
        print bestBetas
        print
        print bestOpts
        print
        print bestRands
        print
        print bestSuccesses

        Writer.writeTourFile(FILENAME, numNodes, bestLength, bestTour)  #CHANGE TO BESTLENGTH, BESTTOUR

    #main()
