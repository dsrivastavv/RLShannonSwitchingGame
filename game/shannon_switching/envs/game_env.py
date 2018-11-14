import gym
from gym import error, spaces, utils
from gym.utils import seeding
from ShannonGraph import ShannonGraph

graph_file = 'graph.txt'


class Env(gym.Env):
    metadata = {'render.modes': ['human']}

    def __init__(self):
        self.ishumanFirstPlayer = 0
        self.ishumanCut = 1
        self.gameGraph = ShannonGraph('graph', self.ishumanCut, self.ishumanFirstPlayer)
        self.numActions = len(self.gameGraph.getEdges())
        self.N = self.gameGraph.N
        self.action_space = spaces.Discrete(self.numActions)
        self.observation_space = spaces.MultiDiscrete([3 for __ in range(self.numActions)])
        self.actionEdgeMap = {}
        self.edgeActionMap = {}
        for i, edge in enumerate(self.gameGraph.edges):
            self.actionEdgeMap[i] = [min(edge[0], edge[1]), max(edge[0], edge[1])]
            self.edgeActionMap[(min(edge[0], edge[1]), max(edge[0], edge[1]))] = i
        self.seed()
        self.reset()

    def step(self, action):
        humanMove = self.actionEdgeMap[action]
        if not self.gameGraph.isPlayableEdge(humanMove):
            return [self.observation, 0, 0, None]
        self.gameGraph.playHumanMove(humanMove)
        idx = self.edgeActionMap[(humanMove[0], humanMove[1])]
        self.observation[idx] = 1
        over = self.gameGraph.isgameover()
        if over == 1:
            return [self.observation, over, 1, None]
        humanMove = [humanMove[0], humanMove[1], humanMove[0] * self.N + humanMove[1]]
        computerMove = self.gameGraph.getComputerMove(humanMove)
        print(computerMove)
        if computerMove[0] != -1:
            self.gameGraph.playComputerMove(computerMove)
            idx = self.edgeActionMap[(computerMove[0], computerMove[1])]
            self.observation[idx] = 2
        over = self.gameGraph.isgameover()
        if over == 0:
            return [self.observation, 0, 0, None]
        else:
            return [self.observation, over, 1, None]

    def reset(self):
        self.observation = [0 for __ in range(self.numActions)]
        self.gameGraph.reset()
        if not self.ishumanFirstPlayer:
            computerMove = self.gameGraph.getComputerMove([0, self.N - 1, self.N * self.N])
            if computerMove[0] != -1:
                self.gameGraph.playComputerMove(computerMove)
                idx = self.edgeActionMap[(computerMove[0], computerMove[1])]
                self.observation[idx] = 2

    def render(self, mode='human', close=False):
        raise NotImplementedError

    def seed(self, seed=None):
        self.np_random, seed = seeding.np_random(seed)
        return [seed]
