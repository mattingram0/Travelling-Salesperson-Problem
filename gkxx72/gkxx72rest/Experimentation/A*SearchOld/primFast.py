import Parser
import sys
import heapq
import time

UPDATED = '<updated-node>'


def main():

    filename = "AISearchfile021.txt"
    distances = Parser.loadSearchFile(filename)  # Distance matrix
    numNodes = len(distances)  # No. of nodes

    unvisited = []
    priorityQueue = []
    entryMap = {}
    shortestNode = {}
    parents = {}
    total = 0

    unvisited.append('0')
    shortestNode['0'] = sys.maxsize
    push(priorityQueue, entryMap, 0, '0')

    for i in range(1, numNodes):
        unvisited.append(str(i))
        shortestNode[str(i)] = sys.maxsize
        push(priorityQueue, entryMap, sys.maxsize, str(i))

    for i in range(numNodes):
        distance, node = pop(priorityQueue, entryMap)
        unvisited.remove(node)
        total += distance

        for child in unvisited:
            dist = distances[int(child)][int(node)]
            if dist < shortestNode[child]:
                push(priorityQueue, entryMap, dist, child)
                parents[child] = node
                shortestNode[child] = dist

    print total


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
