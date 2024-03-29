import networkx as nx
import pkg_resources
import random
import numpy as np

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
				if self.existsEdge([computerMove[0],computerMove[1]]):
					break
		if self.existsEdge([computerMove[0],computerMove[1]]):
			self.updateTrees(humanMove, computerMove, t1, t2)
			return computerMove
		else:
			return [-1, -1, -1]

	def unplayMove(self,edge):
		self.graph[edge[0]][edge[1]]['cut'] = 1
		self.graph[edge[0]][edge[1]]['short'] = self.inf

	def hasHumanWon(self):
		if self.ishumancut:
			return self.hascutwon()
		else:
			return self.hasshortwon()

	def hasComputerWon(self):
		if self.ishumancut:
			return self.hasshortwon()
		else:
			return self.hascutwon()

	def bruteForce(self,player,depth):
		result = -1
		bestEdge = None
		for e in self.graph.edges():
			if not self.isPlayableEdge(e):
				continue
			if player=='human':
				self.playHumanMove(e)
				if self.hasHumanWon():
					result = 1
					bestEdge = e
				elif depth == 0:
					if result == -1:
						result = 0
						bestEdge = e
				else:
					(opponentResult,opponentMove) = self.bruteForce('computer',depth-1)
					if opponentResult == -1:
						result = 1
						bestEdge = e
					elif opponentResult == 0:
						if result == -1:
							result = 0
							bestEdge = e
			else:
				self.playComputerMove(e)
				if self.hasComputerWon():
					result = 1
					bestEdge = e
				elif depth == 0:
					if result == -1:
						result = 0
						bestEdge = e
				else:
					(opponentResult,opponentMove) = self.bruteForce('human',depth-1)
					if opponentResult == -1:
						result = 1
						bestEdge = e
					elif opponentResult == 0:
						if result == -1:
							result = 0
							bestEdge = e
			self.unplayMove(e)
			if result == 1:
				break
		return (result,bestEdge)

	#for Computer
	def evaluationFunction(self,player):
		return 0
		# if self.hasComputerWon():
		# 	return 100
		# elif self.hasHumanWon():
		# 	return -1
		# else:
		# 	heuristic			

	def minimax(self, player, depth, epsilon, alpha, beta):
		legalActions = [e for e in self.graph.edges() if self.isPlayableEdge(e)]
		#print(legalActions)
		if depth == 0:
			print("called")
			value = self.evaluationFunction(player)
			#leaf-node
		else: 
			if np.random.uniform(0.0,1.0)<epsilon:
				legalActions = [legalActions[random.randint(0,len(legalActions)-1)]]
			if player=='human':
				bestVal = float('inf')
				bestEdge = None
				for action in legalActions:
					self.playHumanMove(action)
					if self.hasHumanWon():
						bestVal = -1
						bestEdge = action
						self.unplayMove(action)
						break
					else:
						[oppValue, oppEdge] = self.minimax('computer',depth-1,epsilon,alpha,beta)
						value = 1+ oppValue
						if value < bestVal:
							bestVal = value
							bestEdge = action
						# if bestVal<=alpha:
						# 	self.unplayMove(action)
						# 	break
						beta = min(beta,bestVal)
					self.unplayMove(action)
				return [bestVal,bestEdge]
			else:
				bestVal = float('-inf')
				bestEdge = None
				for action in legalActions:
					self.playComputerMove(action)
					if self.hasComputerWon():
						bestVal = 1000
						bestEdge = action
						#print(legalActions)
						self.unplayMove(action)
						break
					else:
						[oppValue, oppEdge] = self.minimax('human',depth-1,epsilon,alpha,beta)
						value = 1+ oppValue
						if value > bestVal:
							bestVal = value
							bestEdge = action
						# if bestVal>=beta:
						# 	self.unplayMove(action)
						# 	break
						alpha = max(alpha,bestVal)
					self.unplayMove(action)
				return [bestVal,bestEdge]

	def getSelfPlayMove(self,models,gameState,actionEdgeMap):
		l = len(models)
		if l == 0:
			return self.getRandomPlayableEdge()
		r = random.randint(0,l-1)
		action = models[r].step(gameState)[0][0]
		return actionEdgeMap[action]


	def getRandomPlayableEdge(self):
		playableEdges = []
		for e in self.graph.edges():
			if self.isPlayableEdge(e):
				playableEdges.append(e)
		return playableEdges[random.randint(0,len(playableEdges)-1)]	

	def getMinMaxComputerMove(self,epsilon):
		[bestVal, bestEdge] = self.minimax('computer',10000, epsilon, float('-inf'), float('inf'))
		return bestEdge
		# return self.getRandomPlayableEdge()
		# depth = 10
		# (result,bestEdge) = self.bruteForce('computer',depth)
		# if result == -1:
		# 	return self.getRandomPlayableEdge()
		# else:
		# 	return bestEdge

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


	def existsEdge(self, edge):
		return edge in self.graph.edges()

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
