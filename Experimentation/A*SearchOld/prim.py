from Node import Node
import Parser
import sys
import heapq
import time


def main():

    filename = "AISearchfile535.txt"
    distances = Parser.loadSearchFile(filename)  # Distance matrix
    n = len(distances)  # No. of nodes

    priorityQueue = []
    parents = {}
    total = 0

    # Add all vertexes to the pQ - each vertex is name and closest distance
    for i in range(n):
        if i == 0:
            node = Node(str(i), 0)
            heapq.heappush(priorityQueue, node)
        else:
            node = Node(str(i), sys.maxsize)
            heapq.heappush(priorityQueue, node)

    for i in range(n):
        node = heapq.heappop(priorityQueue)
        total += node.dist

        for child in priorityQueue:
            dist = distances[int(child.name)][int(node.name)]
            if dist < child.dist:
                child.dist = dist
                parents[child.name] = node.name
        heapq.heapify(priorityQueue)  # This runs in O(n)

    print total


if __name__ == '__main__':
    startTime = time.time()
    main()
    print str(time.time() - startTime) + " seconds"
