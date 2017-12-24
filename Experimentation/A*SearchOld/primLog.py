from Node import Node
import Parser
import sys
import heapq
import time

# REMEMBER


def main():

    filename = "AISearchfile535.txt"
    distances = Parser.loadSearchFile(filename)  # Distance matrix
    n = len(distances)  # No. of nodes

    unvisited = [str(i) for i in range(n)]
    parents = {}

    priorityQueue = []
    entry_finder = {}               # mapping of tasks to entries
    UPDATED = '<updated-node>'      # placeholder for a UPDATED task

    def push(priorityQueue, node, priority=0):
        if node.name in entry_finder:
            remove(node.name)
        entry = [priority, node]
        entry_finder[node.name] = entry
        heapq.heappush(priorityQueue, entry)

    def remove(name):
        entry = entry_finder.pop(name)
        entry[-1] = UPDATED

    def pop(priorityQueue):
        while priorityQueue:
            priority, node = heapq.heappop(priorityQueue)
            if node is not UPDATED:
                del entry_finder[node.name]
                return node
        raise KeyError('Priority Queue is Empty')

    # Add all vertexes to the pQ - each vertex is name and closest distance
    for i in range(n):
        if i == 0:
            node = Node(str(i), 0)
            push(priorityQueue, node, node.dist)
        else:
            node = Node(str(i), sys.maxsize)
            push(priorityQueue, node, node.dist)

    for i in range(n):
        node = pop(priorityQueue)
        unvisited.remove(node.name)

        for entry in priorityQueue:
            child = entry[-1]
            if not isinstance(child, basestring) and child.name in unvisited:
                dist = distances[int(child.name)][int(node.name)]
                if dist < child.dist:
                    updatedNode = Node(child.name, dist)
                    push(priorityQueue, updatedNode, dist)
                    parents[child.name] = node.name

    total = 0
    for i in range(1, n):
    #     print parents[str(i)] + " - " + str(i) + " : " + str(distances[i][int(parents[str(i)])])
        total += distances[i][int(parents[str(i)])]
    print total


if __name__ == '__main__':
    startTime = time.time()
    main()
    print str(time.time() - startTime) + " seconds"
