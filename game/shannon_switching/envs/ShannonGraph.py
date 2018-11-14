import networkx as nx
import pkg_resources


def readTree(f1, f2):
    files = [f1, f2]
    spanningTree = [None]
    for l in range(2):
        filename = pkg_resources.resource_filename(__name__, files[l])
        with open(filename, "r") as file:
            lines = [line.rsplit() for line in file]
            numedges = int(lines[0][0])
            graph = nx.Graph()
            for i in range(numedges):
                [v1, v2, idx] = [int(x) for x in lines[i + 1]]
                graph.add_edge(v1, v2, index=idx)
            spanningTree.append(graph)
    return spanningTree


def xorOp(spanningTree, e):
    if [e[0], e[1]] in spanningTree.edges():
        spanningTree.remove_edge(e[0], e[1])
    else:
        spanningTree.add_edge(e[0], e[1], index=e[2])
    return spanningTree


# returns list of edges
def findPath(v1, v2, spanningTree):
    l = nx.shortest_path(spanningTree, v1, v2)
    path = []
    for i in range(len(l) - 1):
        path.append([min(l[i], l[i + 1]), max(l[i], l[i + 1]), spanningTree[l[i]][l[i + 1]]['index']])
    return path


class ShannonGraph:
    def __init__(self, filename, ishumancut, ishumanFirstPlayer):
        self.graph = self.inputgraph(filename + '.txt')
        self.ishumancut = ishumancut
        self.ishumanFirstPlayer = ishumanFirstPlayer
        self.edges = self.graph.edges()
        self.N = len(self.graph)
        self.inf = float("inf")
        self.filename = filename
        self.spanningTree = readTree(self.filename + '_tree1.txt', self.filename + '_tree2.txt')

    @staticmethod
    def inputgraph(filename):
        filename = pkg_resources.resource_filename(__name__, filename)
        with open(filename, 'r') as file:
            lines = [line.rsplit() for line in file]
            numedges = int(lines[0][0])
            graph = nx.Graph()
            for i in range(numedges):
                [v1, v2] = [int(x) for x in lines[i + 1]]
                graph.add_edge(v1, v2, short=float("inf"), cut=1)
        return graph

    def updateTrees(self, humanMove, opponentMove, t1, t2):
        if self.ishumancut:
            treeIndex = t1;
        else:
            treeIndex = t2;
        self.spanningTree[treeIndex] = xorOp(self.spanningTree[treeIndex], humanMove)
        self.spanningTree[treeIndex] = xorOp(self.spanningTree[treeIndex], opponentMove)

    # def getEdgeMap(self):
    # 	return [self.edge_map, self.reverse_edge_map]

    def getEdges(self):
        return self.edges

    # humanMove is (v1,v2,index)
    def getComputerMove(self, humanMove):
        [v1, v2, idx] = humanMove
        b1 = [v1, v2] in self.spanningTree[1].edges() and idx == self.spanningTree[1][v1][v2]['index']
        b2 = [v1, v2] in self.spanningTree[2].edges() and idx == self.spanningTree[2][v1][v2]['index']
        if b1 == b2:
            return [-1, -1, -1]
        t1 = 1
        t2 = 2
        if b2:
            t1 = 2
            t2 = 1
        s1 = findPath(v1, v2, self.spanningTree[t2])
        for x in s1:
            s2 = findPath(x[0], x[1], self.spanningTree[t1])
            if humanMove in s2:
                computerMove = x
                break
        self.updateTrees(humanMove, computerMove, t1, t2)
        return computerMove

    # Move will be of form [v1, v2]
    def playHumanMove(self, humanMove):
        if self.ishumancut:
            self.graph[humanMove[0]][humanMove[1]]['cut'] = self.inf
        else:
            self.graph[humanMove[0]][humanMove[1]]['short'] = 1

    # Move will be of form [v1, v2] or pass [-1,-1]
    def playComputerMove(self, opponentMove):
        if opponentMove == [-1, -1]:
            return 0
        else:
            if self.ishumancut:
                self.graph[opponentMove[0]][opponentMove[1]]['short'] = 1
            else:
                self.graph[opponentMove[0]][opponentMove[1]]['cut'] = self.inf
            return 10

    def isPlayableEdge(self, edge):
        return self.graph[edge[0]][edge[1]]['cut'] == 1 and self.graph[edge[0]][edge[1]]['short'] == self.inf

    def reset(self):
        for e in self.graph.edges():
            self.graph[e[0]][e[1]]['short'] = self.inf
            self.graph[e[0]][e[1]]['cut'] = 1
        self.spanningTree = readTree(self.filename + '_tree1.txt', self.filename + '_tree2.txt')

    def hasshortwon(self):
        # find if path exists between source and sink colored by short
        # If path exists it's length is infinity
        # try:
        # 	path_length = nx.shortest_path_length(self.graph, 0, self.graph.number_of_nodes()-1, 'short')
        # 	return True
        # except nx.NetworkXNoPath:
        # 	return False
        path_length = nx.shortest_path_length(self.graph, 0, self.graph.number_of_nodes() - 1, 'short')
        if path_length == self.inf:
            return False
        else:
            return True

    def hascutwon(self):
        # find if path exists between source and sink cut by cut
        # If path exists it's length is infinity
        # try:
        # 	path_length = nx.shortest_path_length(self.graph, 0, self.graph.number_of_nodes()-1, 'cut')
        # 	return False
        # except nx.NetworkXNoPath:
        # 	return True
        path_length = nx.shortest_path_length(self.graph, 0, self.graph.number_of_nodes() - 1, 'cut')
        if path_length == self.inf:
            return True
        else:
            return False

    # returns 1 if human wins, -1 if opponent wins, 0 if game not over
    def isgameover(self):
        if self.ishumancut:
            if self.hascutwon():
                return 1
            elif self.hasshortwon():
                return -1
            else:
                return 0
        else:
            if self.hascutwon():
                return -1
            elif self.hasshortwon():
                return 1
            else:
                return 0
