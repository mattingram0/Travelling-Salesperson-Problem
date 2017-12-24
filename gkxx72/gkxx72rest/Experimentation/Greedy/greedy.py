import Writer
import Parser
import sys

INITIAL_NODE = '0'


def main():

    filename = "AISearchfile012.txt"
    distances = Parser.loadSearchFile(filename)  # Distance matrix
    numNodes = len(distances)
    graph = Parser.createGraph(distances)

    shortestLength = sys.maxsize
    shortestTour = []

    for i in range(numNodes):
        tour, length = nn(graph, numNodes, str(i))
        if length < shortestLength:
            shortestLength = length
            shortestTour = tour

    print shortestTour
    print shortestLength

    Writer.writeTourFile(filename, numNodes, shortestLength, shortestTour)


def nn(graph, numNodes, initial):
    unvisited = [str(i) for i in range(numNodes)]
    pTour = [initial]  # Vary for experimentation
    unvisited.remove(initial)
    minimum = sys.maxsize
    length = 0

    while len(unvisited) != 0:

        minimum = sys.maxsize

        for child in graph.get(pTour[len(pTour) - 1]):  # For each child
            if child.name in unvisited:
                if child.dist < minimum:
                    minimum = child.dist
                    closest = child.name

        length += minimum

        pTour.append(closest)
        unvisited.remove(closest)

    nodes = graph.get(pTour[len(pTour) - 1])

    for node in nodes:
        if node.name == pTour[0]:
            length += node.dist

    return pTour, length


if __name__ == '__main__':
    main()
