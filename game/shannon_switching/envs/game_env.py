import gym
import numpy as np
from gym import error, spaces, utils
from baselines import deepq
from gym.utils import seeding
from .ShannonGraph import ShannonGraph

graphFilePrefix = 'graph'

class Env(gym.Env):
	metadata = {'render.modes': ['human']}

	def __init__(self):
		return None

	def setupShannonGraph(self):
		self.gameGraph = ShannonGraph(graphFilePrefix, self.ishumanCut, self.ishumanFirstPlayer)
		self.numActions = len(self.gameGraph.getEdges())
		self.N = self.gameGraph.N
		self.actionEdgeMap = {}
		self.edgeActionMap = {}
		for i, edge in enumerate(self.gameGraph.edges):
			self.actionEdgeMap[i] = [min(edge[0], edge[1]), max(edge[0], edge[1])]
			self.edgeActionMap[(min(edge[0], edge[1]), max(edge[0], edge[1]))] = i
		print("Shannon graph set up")

	def setupEnvironment(self):
		self.action_space = spaces.Discrete(self.numActions)
		self.observation_space = spaces.MultiDiscrete([3 for __ in range(self.numActions)])
		print("Environment variables set up")

	def setupSelfPlay(self):
		if self.ishumanFirstPlayer and self.ishumanCut:
			self.model = deepq.load_act("model/selfPlay/shannon_switching_train_{}_{}_{}.pkl".format(0, 0, self.iterNo-1))
		elif self.ishumanFirstPlayer and not self.ishumanCut:
			self.model = deepq.load_act("model/selfPlay/shannon_switching_train_{}_{}_{}.pkl".format(0, 1, self.iterNo-1))
		elif not self.ishumanFirstPlayer and self.ishumanCut:
			self.model = deepq.load_act("model/selfPlay/shannon_switching_train_{}_{}_{}.pkl".format(1, 0, self.iterNo-1))
		else:
			self.model = deepq.load_act("model/selfPlay/shannon_switching_train_{}_{}_{}.pkl".format(1, 1, self.iterNo-1))
		print("Self play set up")

	def setupMinMax(self):
		self.epsilon = max(0, 1 - self.iterNo*0.05)
		print("Min max set up with epsilon", self.epsilon)

	def configureEnvironment(self, computerType="random", ishumanFirstPlayer=1, ishumanCut=1, iterNo=0):
		self.computerType = computerType
		self.ishumanFirstPlayer = ishumanFirstPlayer
		self.ishumanCut = ishumanCut
		self.iterNo = iterNo
		self.setupShannonGraph()
		self.setupEnvironment()
		if self.computerType == "selfPlay":
			if iterNo == 0:
				self.computerType = "random"
			else:
				self.setupSelfPlay()
		elif self.computerType == "minMax":
			self.setupMinMax()
		self.seed()
		self.reset()

	# 0: Unplayed edge, 1:cut, 2:connect
	def playHumanMove(self, humanMove):
		self.gameGraph.playHumanMove(humanMove)
		idx = self.edgeActionMap[(humanMove[0], humanMove[1])]
		if self.ishumanCut:
			self.observation[idx] = 1
		else:
			self.observation[idx] = 2
		print('Human Move', humanMove)

	def playComputerMove(self, humanMove):
		if self.computerType == "optimalComputer":
			humanMoveSpanningTree = [humanMove[0], humanMove[1], humanMove[0] * self.N + humanMove[1]]
			computerMove = self.gameGraph.getComputerMove(humanMoveSpanningTree)
		elif self.computerType == "selfPlay":
			computerMove = self.actionEdgeMap[self.model.step(self.observation)[0][0]]
		elif self.computerType == "minMax":
			computerMove = self.gameGraph.getMinMaxComputerMove(self.epsilon)
		elif self.computerType == "random":
			computerMove = self.gameGraph.getRandomPlayableEdge()

		print('Computer Move', computerMove)

		if computerMove[0] != -1:
			self.gameGraph.playComputerMove(computerMove)
			idx = self.edgeActionMap[(computerMove[0], computerMove[1])]
			if self.ishumanCut:
				self.observation[idx] = 2
			else:
				self.observation[idx] = 1
		
	def isGameOver(self):
		over = self.gameGraph.isgameover()
		if over == 0:
			return [self.observation, 0, 0, None]
		else:
			if over == 1:
				print('human won')
			else:
				print('computer won')
			return [self.observation, over*1000, 1, None]

	def step(self, action):
		humanMove = self.actionEdgeMap[action]	# human Move
		if not self.gameGraph.isPlayableEdge(humanMove):
			return [self.observation, 0, 0, None]
		else:
			self.playHumanMove(humanMove)
			if self.gameGraph.isgameover() == 0:
				self.playComputerMove(humanMove)
			return self.isGameOver()
			
	def reset(self):
		self.observation = np.zeros(self.numActions)
		self.gameGraph.reset()
		if not self.ishumanFirstPlayer:
			if self.computerType == "optimalComputer":
				humanMoveSpanningTree = [0, self.N - 1, self.N * self.N]
				computerMove = self.gameGraph.getComputerMove(humanMoveSpanningTree)
				if computerMove[0] != -1:
					self.gameGraph.playComputerMove(computerMove)
					idx = self.edgeActionMap[(computerMove[0], computerMove[1])]
					if self.ishumanCut:
						self.observation[idx] = 2
					else:
						self.observation[idx] = 1
			else:
				self.playComputerMove([-1, -1])
		print('Start state', self.observation)
		return self.observation

	def render(self, mode='human', close=False):
		raise NotImplementedError

	def seed(self, seed=None):
		self.np_random, seed = seeding.np_random(seed)
		return [seed]
