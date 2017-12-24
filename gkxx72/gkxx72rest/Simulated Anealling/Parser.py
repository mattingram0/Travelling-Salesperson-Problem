from Node import Node
import re


def loadSearchFile(name):
    # path = 'J:\DUDE\Desktop\Software Methodologies\AI Search Assignment\Search Files\\' + name
    # path = '/Volumes/gkxx72/DUDE/Desktop/Software Methodologies/AI Search Assignment/Search Files/' + name
    path = '/Users/matt/Documents/Durham/2nd Year/Software Methodologies/AI Search Assignment/checker/cityfiles/' + name
    f = open(path, 'r')
    raw = f.read()

    # TEST SPEED OF THESE TWO
    stripped = "".join(raw.split())
    # stripped = raw.replace(" ", "").replace('\r', '').replace('\n', '')
    split = stripped.split(",")

    namePattern = re.compile("NAME=AISearchfile\d\d\d")
    sizePattern = re.compile("SIZE=\d\d?\d?\d?")

    if not namePattern.match(split[0]) or not sizePattern.match(split[1]):
        print "[-] Error - Name or Size in Incorrect Format"

    for i in range(2, len(split)):
        split[i] = re.sub("\D", "", split[i])

    size = int(split[1][5:])
    distances = [[0 for x in range(size)] for y in range(size)]

    counter = 2
    for i in range(size):
        for j in range(i, size):
            if i != j:
                distances[i][j], distances[j][i] = int(
                    split[counter]), int(split[counter])  # style
                counter += 1

    # print distances

    return distances


def createGraph(distances):
    graph = {}
    nodes = []

    for i in range(len(distances)):
        for j in range(len(distances)):
            if i != j:
                node = Node(str(j), distances[i][j])
                nodes.append(node)
        graph[str(i)] = nodes
        nodes = []

    return graph