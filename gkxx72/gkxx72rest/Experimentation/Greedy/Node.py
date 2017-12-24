class Node:

    def __init__(self, name, dist):
        self.name = name
        self.dist = dist

    def __cmp__(self, other):
        return cmp(self.dist, other.dist)

