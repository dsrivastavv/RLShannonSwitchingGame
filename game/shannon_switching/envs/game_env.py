import networkx as nx



def inputTree(fileName):
	with open(fileName, 'r') as f:
		lines = [line.rsplit() for line in f]
		numLines = len(lines)
		for i in 

def initialize_game_state(graph):
	N = len(graph[0])
	state = [[1 0 0 0] for i in range(N*N)]
	for i in range(N):
		for j in range(i+1,N):
			if graph[i][j]:
				state[i*N+j] = [0 1 0 0]
	return state

def xorOp(spanningTree, e):
	if e in spanningTree:
		spanningTree.remove(e)
	else:
		spanningTree.append(e)
	return spanningTree



GameGraph = ShanonGraph(0)

#state is a configuration of the graph 
class Env(gym.Env):
	metadata = {'render.modes': ['human']}

	def __init__(self):
		self.seed()
		self.reset()

	#action is edge [v1,v2]
	def step(self, action):
		GameGraph.playHumanMove(action)
		x = isGameOver()
		if not x==0:
			return [GameGraph.getState(), x, 1, {}]
		else:
			opponentMove = GameGraph.getComputerMove(action) #call updateTree inside this function
			GameGraph.playOpponentMove(opponentMove)
			y = isGameOver()
			if not y==0:
				return [GameGraph.getState(), y, 1, {}]
			else:
				return [GameGraph.getState(), 0, 0, {}] 

	def reset(self):
		GameGraph.reset()

	def render(self, mode='human', close=False):
		raise NotImplementedError

	def seed(self, seed=None):
		self.np_random, seed = seeding.np_random(seed)
		return [seed]	