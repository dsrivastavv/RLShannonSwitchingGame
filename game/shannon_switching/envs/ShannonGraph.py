import networkx as nx


class ShanonGraph:

    @staticmethod
    def inputgraph(filename):
        with open(filename, 'r') as file:
            lines = [line.rsplit() for line in file]
            numedges = int(lines[0][0])
            graph = nx.Graph()
            for i in range(numedges):
                [v1, v2] = [int(x) for x in lines[i + 1]]
                graph.add_edge(v1, v2, short=float("inf"), cut=1)
        return graph

    def __init__(self, filename, ishumancut):
        self.graph = self.inputgraph(filename)
        self.ishumancut = ishumancut
        self.edges = self.graph.edges
        self.inf = float("inf")

    # Move will be of form [v1, v2]
    def playhumanmove(self, humanmove):
        if self.graph[humanmove[0]][humanmove[1]]['cut'] == 1 and self.graph[humanmove[0]][humanmove[1]]['short'] == self.inf:
            if self.ishumancut:
                self.graph[humanmove[0]][humanmove[1]]['cut'] = self.inf
            else:
                self.graph[humanmove[0]][humanmove[1]]['short'] = 1
            return 1
        else:
            return 0

    # Move will be of form [v1, v2]
    def playcomputermove(self, opponentmove):
        if self.graph[opponentmove[0]][opponentmove[1]]['cut'] == 1 and self.graph[opponentmove[0]][opponentmove[1]]['short'] == self.inf:
            if self.ishumancut:
                self.graph[opponentmove[0]][opponentmove[1]]['short'] = 1
            else:
                self.graph[opponentmove[0]][opponentmove[1]]['cut'] = self.inf
            return 1
        else:
            return 0

    def reset(self):
        for e in self.graph.edges():
            self.graph[e[0]][e[1]]['short'] = self.inf
            self.graph[e[0]][e[1]]['cut'] = 1

    def hasshortwon(self):
        # find if path exists between source and sink colored by short
        # If path exists it's length is infinity
        path_length = nx.shortest_path_length(self.graph, 1, self.graph.number_of_nodes(), 'short')
        if path_length == self.inf:
            return False
        else:
            return True

    def hascutwon(self):
        # find if path exists between source and sink cut by cut
        # If path exists it's length is infinity
        path_length = nx.shortest_path_length(self.graph, 1, self.graph.number_of_nodes(), 'cut')
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
