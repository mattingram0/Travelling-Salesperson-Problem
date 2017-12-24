from PartialTour import PartialTour
from Node import Node
from Vertex import Vertex
import Writer
import Parser
import sys
import heapq
import time

UPDATED = '<updated-node>'

def main():

    filename = "AISearchfile017.txt"
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

                expand(pTour, children, graph, numNodes, pQueue, distances)  # Exp frntier

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


def expand(pTour, children, graph, numNodes, pQueue, distances):

    for child in children:  # For each child of the node

        if child.name not in pTour.path:  # If child not already in the p. tour

            gNew = pTour.g + child.dist  # Calc cost to child
            hNew = mstHeuristicAdmiss(child, pTour, graph, numNodes, distances)
            #hNew = heuristicNNDTS(child, pTour, graph, distances)
            #hNew = mstHeuristicLog(distances, child, pTour)

            fNew = gNew + hNew

            pathNew = []

            if(pTour.endNode != ""):  # If not []
                pathNew.extend(pTour.path)
                pathNew.append(pTour.endNode)

            pTourNew = PartialTour(  # Create new partial tour
                child.name, fNew, gNew, hNew, pathNew)

            heapq.heappush(pQueue, pTourNew)


def heuristicSLD(child, pTour, graph):  # Chooses child closest to first node

    h = 0

    for node in graph.get(pTour.path[0]):
        if node.name == child.name:
            h = node.dist

    return h


def mstHeuristicQuadratic(child, pTour, numNodes, graph):  # Chooses mst NON ADMISSABLE

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


def mstHeuristicLinear(distances, child, pTour):  # Prim, O(e + elogv) ?
    numNodes = len(distances)  # No. of nodes

    priorityQueue = []
    parents = {}

    # Add all vertexes to the pQ - each vertex is name and closest distance
    counter = 0
    for i in range(numNodes):
        if str(i) not in pTour.path and str(i) != child.name and str(
                i) != pTour.endNode:  # i.e if unvisited
            if counter == 0:  # i.e ensure first node added gets popped
                vertex = Vertex(str(i), 0)
                heapq.heappush(priorityQueue, vertex)
            else:
                vertex = Vertex(str(i), sys.maxsize)
                heapq.heappush(priorityQueue, vertex)
        counter += 1

    total = 0

    for i in range(len(priorityQueue)):
        node = heapq.heappop(priorityQueue)
        total += node.dist

        for vertex in priorityQueue:
            dist = distances[int(vertex.name)][int(node.name)]
            if dist < vertex.dist:
                vertex.dist = dist
                parents[vertex.name] = node.name
        heapq.heapify(priorityQueue)  # This runs in O(n)

    return total


def mstHeuristicLog(distances, child, pTour, unvisit=[]):  # Non admissable
    numNodes = len(distances)

    priorityQueue = []
    entryMap = {}
    shortestNode = {}
    parents = {}
    total = 0
    unvisited = unvisit[:]

    if not unvisited:  # i.e if running as own heuristic, generate own unvisit list
        for i in range(numNodes):  # TEST BELOW
            if str(i) not in pTour.path and str(i) != child.name and str(
                    i) != pTour.endNode:
                unvisited.append(str(i))
                shortestNode[str(i)] = sys.maxsize
                push(priorityQueue, entryMap, sys.maxsize, str(i))
    else:
        for i in unvisited:
            shortestNode[i] = sys.maxsize

    if len(unvisited) == 0:  # BREAK OUT EARLY - TEST
        return 0

    push(priorityQueue, entryMap, 0, unvisited[0])  # make 1st unvisit node pop

    for i in range(len(unvisited)):
        distance, node = pop(priorityQueue, entryMap)
        unvisited.remove(node)
        total += distance

        for child in unvisited:
            dist = distances[int(child)][int(node)]
            if dist < shortestNode[child]:
                push(priorityQueue, entryMap, dist, child)
                parents[child] = node
                shortestNode[child] = dist

    return total


def mstHeuristicAdmiss(child, pTour, graph, numNodes, distances):

    distToNeighbour = heuristicNN(child, pTour, graph)

    unvisited = []

    for i in range(numNodes):  # TEST BELOW
        if str(i) not in pTour.path and str(i) != child.name and str(
                i) != pTour.endNode:
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

    mst = mstHeuristicLog(distances, child, pTour, unvisited)

    return distToNeighbour + mst + distToStart


def heuristicNN(child, pTour, graph):  # Chooses nearest neighbour

    visited = []
    visited.extend(pTour.path)

    # TEST THIS
    if pTour.endNode != "":
        visited.append(pTour.endNode)

    visited.append(child.name)

    minimum = sys.maxsize

    for node in graph.get(child.name):
        if node.name not in visited:
            # print "Child Not Visited : " + node.name + " | Distance: " + str(node.dist)
            if node.dist < minimum:
                minimum = node.dist

    return minimum

def heuristicNNDTS(child, pTour, graph, distances):  # Chooses nearest neighbour and shortest
                                                     # distances to the start
    visited = []
    visited.extend(pTour.path)
    selected = ""
    total = 0

    if pTour.endNode != "":
        visited.append(pTour.endNode)

    visited.append(child.name)

    minimum = sys.maxsize

    for node in graph.get(child.name):  # Find closest node to end
        if node.name not in visited:
            if node.dist < minimum:
                minimum = node.dist
                selected = node.name

    total += minimum

    visited.append(selected)

    minimum = sys.maxsize

    for node in graph.get(child.name):  # Find closest node to start
        if node.name not in visited:
            dist = distances[int(pTour.path[0])][int(node.name)]
            if dist < minimum:
                minimum = dist

    total += minimum

    return total


def heuristicGC(child, graph):  # Greedy completion, unfinished

    nodelist = []

    for node in graph.get(child.name):
        heapq.heappush(nodelist, node)


def push(pQueue, entryMap, shortestDist, node): 
    if node in entryMap:
        entry = entryMap.pop(node)
        entry[-1] = UPDATED

    entry = [shortestDist, node]
    entryMap[node] = entry
    heapq.heappush(pQueue, entry)


def pop(pQueue, entryMap):
    while pQueue:
        priority, node = heapq.heappop(pQueue)
        if node != UPDATED:
            del entryMap[node]
            return priority, node


if __name__ == '__main__':
    startTime = time.time()
    main()
    print str(time.time() - startTime) + " seconds"
