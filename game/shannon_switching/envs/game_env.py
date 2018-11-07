# import gym
# from gym import error, spaces, utils
# from gym.utils import seeding
from ShanonnGraph import ShannonGraph
import Queue
graph_file = 'graph.txt'


def initialize_game_state(graph):
	N = len(graph[0])
	state = [[1 0 0 0] for i in range(N*N)]
	for i in range(N):
		for j in range(i+1,N):
			if graph[i][j]:
				state[i*N+j] = [0 1 0 0]
	return state

GameGraph = ShannonGraph('graph',0)

#state is a configuration of the graph 
class Env(gym.Env):
	metadata = {'render.modes': ['human']}

	def __init__(self):
		self.numEdges = len(GameGraph.getEdges())
		self.edges = GameGraph.getEdges()
		self.N = GameGraph.N
		self.action_space = spaces.Discrete(numEdges)
		self.observation_space = spaces.MultiDiscrete([3 for i in range(numEdges)])
		self.ishumanFirstPlayer = GameGraph.ishumanFirstPlayer
		#[self.edge_map, self.reverse_edge_map] = GameGraph.getEdgeMap()
		self.seed()
		self.reset()
	#action is a number 
	def step(self, action):
		[v1,v2] = self.edges[action]	
		humanMove = [min(v1,v2),max(v1,v2)]
		if not GameGraph.isPlayableEdge(humanMove):
			return [self.observation,0,0,None]
		GameGraph.playHumanMove(humanMove)
		idx = self.edges.index([computerMove[0],computerMove[1]])
		self.observation[idx]=1 #humanPlay
		over = GameGraph.isgameover()
		if over!=0:
			return [self.observation,over,1,None]
		humanMove = [v1,v2,v1*self.N+v2]
		computerMove = GameGraph.getComputerMove(humanMove)
		if computerMove[0]!=-1:
			GameGraph.playComputerMove(computerMove)
			idx = self.edges.index([computerMove[0],computerMove[1]])
			self.observation[idx]=2

		over = GameGraph.isgameover()
		if over==0:
			return [self.observation,0,0,None]
		else:
			return [self.observation,over,1,None]	


	def reset(self):
		self.observation = [0 for i in range(self.numEdges)] #0 means edge is not played, 1 means edge is played by human, 2 means edge played by computer
		if not self.ishumanFirstPlayer:
			computerMove = GameGraph.getComputerMove([0,self.N-1,self.N*self.N])
			if computerMove[0]!=-1:
				GameGraph.playComputerMove(computerMove)
				idx = self.edges.index([computerMove[0],computerMove[1]])
				self.observation[idx]=2
		GameGraph.reset()

	def render(self, mode='human', close=False):
		raise NotImplementedError

	def seed(self, seed=None):
		self.np_random, seed = seeding.np_random(seed)
		return [seed]	