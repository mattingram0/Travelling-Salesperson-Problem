from PartialTourModG import PartialTourModG
from Node import Node
import Writer
import Parser
import sys

import re
import heapq

# CONSIDER ROTATING WHICH NODE WE START FROM, EXPERIMENTAL
# CHANGING HEURISTICS - MST, 
# USING SUB OPTIMAL, SUB ADMISSABLE HEURISTICS

graph = {}  # The connected graph of nodes, implemented a dictionary
pQueue = []  # The frontier, implemented as a prioirity queue
tour = []  # A full tour of the graph
length = 0  # Length of the full tour
n = 0


def run():

    global graph
    filename = "AISearchfile017.txt"
    global tour
    global length
    global pQueue
    global n

    distances = Parser.loadSearchFile(filename)  # Distance matrix
    n = len(distances)  # No. of nodes

    graph = Parser.createGraph(distances)

    pTour = PartialTourModG()  # Create the empty partial tour

    heapq.heappush(pQueue, pTour)  # Add initial partial tour to the frontier

    while(True):

        if not pQueue:  # Check if Frontier is Empty
            return

        else:

            pTour = heapq.heappop(pQueue)  # Get the most optimal pTour
            # outPath = []
            # outPath.extend(pTour.path)
            # print outPath
            # print "g: " + str(pTour.g) + " - h: " + str(pTour.h)
            # print

            if len(pTour.path) < (n - 1):  # If not a full tour

                if pTour.endNode == "":  # If pTour = []
                    children = [Node(str(i), 0) for i in range(n)]
                else:
                    children = graph.get(pTour.endNode)  # Get all children

                expand(pTour, children)  # Expand the frontier

            else:  # If a full tour, i.e ensuring goal node not expanded
                tour = pTour.path
                tour.append(pTour.endNode)
                tour = [str(int(i) + 1) for i in tour]  # start at 1 not 0

                for node in graph.get(str(int(tour[0]) - 1)):  # FUCKING -1
                    if node.name == pTour.endNode:
                        length = pTour.lth + node.dist
                break

    Writer.writeTourFile(filename, n, length, tour)
    tourString = ",".join(str(t) for t in tour)
    print "Start Location: " + tour[0] + " - Distance: " + str(length) + " - Tour: " + tourString


def expand(pTour, children):
    global graph

    for child in children:  # For each child of the node

        if child.name not in pTour.path:  # If child not already in the p. tour

            lNew = pTour.lth + child.dist  # Calc cost to child
            # hNew = heuristicSLD(child)  # Estimate cost back to start
            # hNew = heuristicNN(child, pTour)  # Nearest node
            # hNew = heuristicMST(child, pTour)  # Est min cost of rest of node
            # = heuristicMSTA(child, pTour)

            hNew = 0
            fNew = child.dist + hNew

            pathNew = []

            if(pTour.endNode != ""):  # If not []
                pathNew.extend(pTour.path)
                pathNew.append(pTour.endNode)

            pTourNew = PartialTourModG(  # Create new partial tour
                child.name, fNew, lNew, hNew, pathNew)

            heapq.heappush(pQueue, pTourNew)


def heuristicSLD(child, pTour):  # Chooses child closest to first node

    global graph

    h = 0

    for node in graph.get(pTour.path[0]):
        if node.name == child.name:
            h = node.dist

    return h


def heuristicMST(child, pTour):  # Chooses min spanning tree NON ADMISSABLE

    global n

    h = 0

    mst = []
    unvisited = []

    mst.append(child.name)

    for i in range(n):
        if str(i) not in pTour.path and str(i) != child.name:
            unvisited.append(str(i))

    # print "Visited: [" + ",".join(pTour.path) + "]"
    # print "Node: " + child.name
    # print "Unvisited: [" + ",".join(unvisited) + "]"

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

    #ALT IMPLEMENTATION

    # visited = []
    # nodelist = []
    # mst = []

    # visited.extend(pTour.path)
    # visited.append(child.name)

    # mst.append(child.name)

    # while len(visited) < n:
    #     for node in mst:
    #         for child in graph.get(node):
    #             if child.name not in visited:
    #                 heapq.heappush(nodelist, child)

    #     closest = heapq.heappop(nodelist)
    #     visited.append(closest.name)
    #     mst.append(closest.name)

    #     h += closest.dist

    # return h


def heuristicMSTA(child, pTour):  # Chooses min spanning tree ADMISSABLE

    global n
    global graph

    distToNeighbour = heuristicNN(child, pTour)

    mst = []
    unvisited = []

    for i in range(n):  # TEST BELOW
        if str(i) not in pTour.path and str(i) != child.name and str(i) != pTour.endNode:
            unvisited.append(str(i))

    if len(unvisited) == 0:  # BREAK OUT EARLY - TEST
        return 0

    # print "Final Node So Far: " + child.name
    # print "Unvisited Cities: [" + " ".join(unvisited) + "]"

    distToStart = sys.maxsize

    # TEST BELOW
    if len(pTour.path) == 0 and pTour.endNode == "":  # i.e if pTour == []
        distToStart = 0
    else:
        if len(pTour.path) == 0:  # if pTour = [1] but path = []
            # print "Start Node: " + pTour.endNode
            startNeighbours = graph.get(pTour.endNode)
        else:  # if path = [i, ...]
            # print "Start Node: " + pTour.path[0]
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
        while len(localUnvisited) != 0:  # While there are still unvisited nodes

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

    # print "Distance to Nearest City: " + str(distToNeighbour)
    # print "Minimum SPanning Tree Length: " + str(overallMin)
    # print "Distance Back to Start: " + str(distToStart)

    # print "h: " + str(distToNeighbour + overallMin + distToStart)
    # print

    return distToNeighbour + overallMin + distToStart


def heuristicNN(child, pTour):  # Chooses nearest neighbour

    global graph

    visited = []
    visited.extend(pTour.path)

    # TEST THIS
    if pTour.endNode != "":
        visited.append(pTour.endNode)
    
    visited.append(child.name)

    minimum = sys.maxsize

    # print "Visited Cities: [" + " ".join(visited) + "]"

    #CHANGE BACK

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




def heuristicGC(child):  # Greedy completion
    
    global graph

    nodelist = []

    for node in graph.get(child.name):
        heapq.heappush(nodelist, node)



















































# for key in graph.keys():

#         print key + ": "
#         nodes = graph[key]

#         for node in nodes:
#             print node.name + " : " + str(node.dist)
#         print ""
