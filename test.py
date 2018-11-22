import gym
import shannon_switching
from baselines import deepq
from baselines.common import models
import pickle
from gym.envs.registration import register
import tensorflow as tf
import sys

def callback(lcl, _glb):
	print(lcl)
	return False
	
def main():
	# setup environment
	computerType = sys.argv[1]
	ishumanFirstPlayer = int(sys.argv[2])
	ishumanCut = int(sys.argv[3])
	fileName = sys.argv[4]
	env = gym.make('shannon_switching-v0')
	env.configureEnvironment(computerType=computerType, ishumanFirstPlayer=ishumanFirstPlayer, 
		ishumanCut=ishumanCut, iterNo=20, epsilon=0.2)
	print("ishumanFirstPlayer ", ishumanFirstPlayer)
	print("ishumanCut", ishumanCut)
	model = deepq.load_act(fileName)
	totalIterations = 2000
	totalWins = 0
	for i in range(totalIterations):
		print(i)
		state = env.reset()
		while True:
			state, reward, isOver, __ = env.step(model.step(state)[0][0])
			if isOver!=0:
				break
		if reward == 1000:
			totalWins += 1
	print("Accuracy: ", totalWins/totalIterations)

if __name__ == '__main__':
	main()
