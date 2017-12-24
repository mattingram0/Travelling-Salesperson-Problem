class PartialTour:

    def __init__(self, endNode="", f=0, g=0, h=0, path=[]):
        self.endNode = endNode
        self.f = f
        self.g = g
        self.h = h
        self.path = path

    def __cmp__(self, other):
        return cmp(self.f, other.f)

