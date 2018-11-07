# import gym
# from gym import error, spaces, utils
# from gym.utils import seeding
from ShanonnGraph import ShanonGraph
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

GameGraph = ShanonGraph('graph',0)

#state is a configuration of the graph 
class Env(gym.Env):
	metadata = {'render.modes': ['human']}

	def __init__(self):
		self.numEdges = len(GameGraph.getEdges())
		self.N = GameGraph.N
		self.action_space = spaces.Discrete(numEdges)
        self.observation_space = spaces.MultiDiscrete([3 for i in range(numEdges)])
        [self.edge_map, self.reverse_edge_map] = GameGraph.getEdgeMap()
		self.seed()
		self.reset()
	#action is a number 
	def step(self, action):
		v1 = action/N
		v2 = action%N
		

	def reset(self):
		self.observation = [0 for i in range(self.numEdges)]
		GameGraph.reset()

	def render(self, mode='human', close=False):
		raise NotImplementedError

	def seed(self, seed=None):
		self.np_random, seed = seeding.np_random(seed)
		return [seed]	