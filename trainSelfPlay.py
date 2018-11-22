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
	ishumanFirstPlayer = int(sys.argv[1])
	ishumanCut = int(sys.argv[2])
	iterNo = int(sys.argv[3])
	env = gym.make('shannon_switching-v0')
	env.configureEnvironment(computerType="selfPlay", ishumanFirstPlayer=ishumanFirstPlayer, 
		ishumanCut=ishumanCut, iterNo=iterNo)
	print("Computer Type: ", "selfPlay")
	print("ishumanFirstPlayer ", ishumanFirstPlayer)
	print("ishumanCut", ishumanCut)
	print("iterNo", iterNo)
	# input("Press Enter to continue...")

	# train network
	act = deepq.learn(
		env,
		network=models.mlp(num_hidden=40, num_layers=10),
		lr=5e-4,
		total_timesteps=50,
		buffer_size=5000,
		exploration_fraction=0.1,
		exploration_final_eps=0.02,
		print_freq=1,
		param_noise=False,
		prioritized_replay=True,
	)
	print("Saving model to model/selfPlay/shannon_switching_{}_{}_{}.pkl".format(ishumanFirstPlayer, ishumanCut, iterNo))
	act.save("model/selfPlay/shannon_switching_{}_{}_{}.pkl".format(ishumanFirstPlayer, ishumanCut, iterNo))
	act.save_act("model/selfPlay/shannon_switching_train_{}_{}_{}.pkl".format(ishumanFirstPlayer, ishumanCut, iterNo))

if __name__ == '__main__':
	main()



