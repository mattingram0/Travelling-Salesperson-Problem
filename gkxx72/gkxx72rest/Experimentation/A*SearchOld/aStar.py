# CHANGE ALL END VALUE ARRAY FINDINGS USING LENGTH TO USE -1 INSTEAD - PYTHONICm ''
from PartialTour import PartialTour
from Node import Node
import Writer
import Parser
import sys
import heapq
import time

# CONSIDER ROTATING WHICH NODE WE START FROM, EXPERIMENTAL
# CHANGING HEURISTICS - MST,
# USING SUB OPTIMAL, SUB ADMISSABLE HEURISTICS


def main():

    filename = "AISearchfile021.txt"
    pQueue = []

    distances = Parser.loadSearchFile(filename)  # Distance matrix
    numNodes = len(distances)  # No. of nodes

    graph = Parser.createGraph(distances)

    pTour = PartialTour()  # Create the empty partial tour

    heapq.heappush(pQueue, pTour)  # Add initial partial tour to the frontier

    while(True):

        if not pQueue:  # Check if Frontier is Empty
            return

        else:

            pTour = heapq.heappop(pQueue)  # Get the most optimal pTour

            if len(pTour.path) < (numNodes - 1):  # If not a full tour

                if pTour.endNode == "":  # If pTour = []
                    children = [Node(str(i), 0) for i in range(numNodes)]
                else:
                    children = graph.get(pTour.endNode)  # Get all children

                expand(pTour, children, graph, numNodes, pQueue)  # Exp frntier

            else:  # If a full tour, i.e ensuring goal node not expanded
                tour = pTour.path
                tour.append(pTour.endNode)
                tour = [str(int(i) + 1) for i in tour]  # start at 1 not 0

                for node in graph.get(str(int(tour[0]) - 1)):  # FUCKING -1
                    if node.name == pTour.endNode:
                        length = pTour.g + node.dist
                break

    Writer.writeTourFile(filename, numNodes, length, tour)
    tourString = ",".join(str(t) for t in tour)
    print "Start Location: " + tour[0] + " - Distance: " + str(
        length) + " - Tour: " + tourString


def expand(pTour, children, graph, numNodes, pQueue):

    for child in children:  # For each child of the node

        if child.name not in pTour.path:  # If child not already in the p. tour

            gNew = pTour.g + child.dist  # Calc cost to child
            hNew = heuristicMSTA(child, pTour, graph, numNodes)

            fNew = gNew + hNew

            pathNew = []

            if(pTour.endNode != ""):  # If not []
                pathNew.extend(pTour.path)
                pathNew.append(pTour.endNode)

            pTourNew = PartialTour(  # Create new partial tour
                child.name, fNew, gNew, hNew, pathNew)

            heapq.heappush(pQueue, pTourNew)


def heuristicSLD(child, pTour, graph):  # Chooses child closest to first node

    global graph

    h = 0

    for node in graph.get(pTour.path[0]):
        if node.name == child.name:
            h = node.dist

    return h


def mstHeuristicQuadratic(child, pTour, numNodes):  # Chooses mst NON ADMISSABLE

    h = 0

    mst = []
    unvisited = []

    mst.append(child.name)

    for i in range(numNodes):
        if str(i) not in pTour.path and str(i) != child.name:
            unvisited.append(str(i))

    while len(unvisited) != 0:  # While there are still unvisited nodes

        minimum = sys.maxsize

        # Find the closest node:

        for node in mst:  # For every node in MST so far
            for child in graph.get(node):  # For each node in children
                if child.name in unvisited:
                    if child.dist < minimum:
                        minimum = child.dist
                        closest = child.name

        h += minimum

        mst.append(closest)
        unvisited.remove(closest)

    return h


def mstHeuristicLinear(distances):  # Prim, O(e + elogv) ?
    numNodes = len(distances)  # No. of nodes

    priorityQueue = []
    parents = {}

    # Add all vertexes to the pQ - each vertex is name and closest distance
    for i in range(numNodes):
        if i == 0:
            node = Node(str(i), 0)
            heapq.heappush(priorityQueue, node)
        else:
            node = Node(str(i), sys.maxsize)
            heapq.heappush(priorityQueue, node)

    for i in range(numNodes):
        node = heapq.heappop(priorityQueue)

        for child in priorityQueue:
            dist = distances[int(child.name)][int(node.name)]
            if dist < child.dist:
                child.dist = dist
                parents[child.name] = node.name
        heapq.heapify(priorityQueue)  # This runs in O(n)

    total = 0
    for i in range(1, numNodes):
        total += distances[i][int(parents[str(i)])]
    return total


def heuristicMSTA(child, pTour, graph, numNodes):  # To unvisit, MST, to start

    distToNeighbour = heuristicNN(child, pTour)

    mst = []
    unvisited = []

    for i in range(numNodes):  # TEST BELOW
        if str(i) not in pTour.path and str(i) != child.name and str(i) != pTour.endNode:
            unvisited.append(str(i))

    if len(unvisited) == 0:  # BREAK OUT EARLY - TEST
        return 0

    distToStart = sys.maxsize
    # TEST BELOW
    if len(pTour.path) == 0 and pTour.endNode == "":  # i.e if pTour == []
        distToStart = 0
    else:
        if len(pTour.path) == 0:  # if pTour = [1] but path = []
            startNeighbours = graph.get(pTour.endNode)
        else:  # if path = [i, ...]
            startNeighbours = graph.get(pTour.path[0])
        for city in unvisited:
            for node in startNeighbours:
                if city == node.name and node.dist < distToStart:
                    distToStart = node.dist

    overallMin = sys.maxsize

    for i in range(len(unvisited)):

        localUnvisited = unvisited[:]
        localMst = mst[:]
        minTree = 0
        localMst.append(localUnvisited[i])
        localUnvisited.remove(localUnvisited[i])
        while len(localUnvisited) != 0:  # While there are still unvisit nodes

            minimum = sys.maxsize  # A very big number

            # Find the closest node:

            for node in localMst:  # For every node in MST so far
                for child in graph.get(node):  # For each node in children
                    if child.name in localUnvisited:
                        if child.dist < minimum:
                            minimum = child.dist
                            closest = child.name

            minTree += minimum

            localMst.append(closest)
            localUnvisited.remove(closest)

        if minTree < overallMin:
            overallMin = minTree

    return distToNeighbour + overallMin + distToStart


def heuristicNN(child, pTour, graph):  # Chooses nearest neighbour

    visited = []
    visited.extend(pTour.path)

    # TEST THIS
    if pTour.endNode != "":
        visited.append(pTour.endNode)

    visited.append(child.name)

    minimum = sys.maxsize


    # CHANGE BACK

    # for node in visited:
    #     for child in graph.get(node):
    #         if child.name not in visited:
    #             print "Node Visited: " + node + " | Child Not Visited : " + child.name + " | Distance: " + str(child.dist)
    #             if child.dist < minimum:
    #                 minimum = child.dist

    for node in graph.get(child.name):
        if node.name not in visited:
            # print "Child Not Visited : " + node.name + " | Distance: " + str(node.dist)
            if node.dist < minimum:
                minimum = node.dist

    return minimum

    # Alt Imp:

    # nodelist = []

    # for node in graph.get(child.name):
    #     if node.name not in visited:
    #         heapq.heappush(nodelist, node)

    # return heapq.heappop(nodelist).dist


def heuristicGC(child, graph):  # Greedy completion

    nodelist = []

    for node in graph.get(child.name):
        heapq.heappush(nodelist, node)


if __name__ == '__main__':
    startTime = time.time()
    main()
    print str(time.time() - startTime) + " seconds"

