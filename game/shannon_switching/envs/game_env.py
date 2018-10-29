import gym
from gym import error, spaces, utils
from gym.utils import seeding

class Env(gym.Env):
	metadata = {'render.modes': ['human']}

	def __init__(self):
		return true

	def step(self, action):
		raise NotImplementedError

	def reset(self):
		raise NotImplementedError

	def render(self, mode='human', close=False):
		raise NotImplementedError	