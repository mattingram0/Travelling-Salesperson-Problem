class PartialTourModG:

    def __init__(self, endNode="", f=0, lth=0, h=0, path=[]):
        self.endNode = endNode
        self.f = f
        self.h = h
        self.lth = lth
        self.path = path

    def __cmp__(self, other):
        return cmp(self.f, other.f)

