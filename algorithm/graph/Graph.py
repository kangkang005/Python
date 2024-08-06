from Vertex import Vertex
import graphviz

class Graph:
    def __init__(self):
        self.vertList = {}
        self.numVertices = 0

    def addVertex(self, key):
        self.numVertices = self.numVertices + 1
        newVertex = Vertex(key)
        self.vertList[key] = newVertex
        return newVertex

    def getVertex(self, n):
        if n in self.vertList:
            return self.vertList[n]
        return None

    def __contains__(self, n):
        return n in self.vertList

    def addEdge(self, f, t, cost=0):
        # add non-existent vertex
        if f not in self.vertList:
            nv = self.addVertex(f)
        if t not in self.vertList:
            nv = self.addVertex(t)
        self.vertList[f].addNeighbor(self.vertList[t], cost)

    def getVertices(self):
        return self.vertList.keys()

    def __iter__(self):
        return iter(self.vertList.values())

    def print_graph(self):
        # Digraph class is directed graph, Graph class is undirected graph
        g = graphviz.Digraph("Demo")
        # g = graphviz.Graph("Demo", filename="Demo.gv")
        # g = graphviz.Graph("Demo")

        # rankdir Corresponding to directed graphs drawn from top to bottom, from left to right, from bottom to top, and from right to left, respectively.
        g.attr(rankdir='LR', size='8,5')
        for vert in self.vertList.values():
            g.node(str(vert.getId()))
        for vert in self.vertList.values():
            for other_vert in vert.getConnections():
                g.edge(str(vert.getId()), str(other_vert.getId()), label=str(vert.getWeight(other_vert)))
        g.view()
        g.render()