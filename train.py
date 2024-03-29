import gym
import shannon_switching
from baselines import deepq
from baselines.common import models
import pickle
from gym.envs.registration import register
import tensorflow as tf
import sys

# def callback(lcl, _glb):
	# stop training if reward exceeds 199
	# is_solved = lcl['t'] > 100 and sum(lcl['episode_rewards'][-101:-1]) / 100 >= 1000
	# # print(lcl)
	# return is_solved
	
def main():
	iterNo = int(sys.argv[1])
	trainPlayer = sys.argv[2]
	print('iterNo:',iterNo)
	print('trainPlayer:',trainPlayer)
	if trainPlayer=='cut':
		register(
		id='shannon_switching-v0',
		entry_point='shannon_switching.envs:Env',
		kwargs={'ishumanFirstPlayer':1, 'ishumanCut':1, 'iterNo':iterNo}
		)
	elif trainPlayer=='connect':
		register(
		id='shannon_switching-v0',
		entry_point='shannon_switching.envs:Env',
		kwargs={'ishumanFirstPlayer':1, 'ishumanCut':0, 'iterNo':iterNo}
		)
	env = gym.make('shannon_switching-v0')
	act = deepq.learn(
		env,
		network=models.mlp(num_hidden=14,num_layers=2),
		lr=5e-4,
		total_timesteps=25000,
		buffer_size=50000,
		exploration_fraction=0.1,
		exploration_final_eps=0.02,
		print_freq=1,
		param_noise=False,
		prioritized_replay=True,
		load_path='shannon_switching_{}_{}.pkl'.format(trainPlayer,iterNo-1) if iterNo > 0 else None,
	)
	print("Saving model to shannon_switching_{}_{}.pkl".format(trainPlayer,iterNo))
	act.save("shannon_switching_{}_{}.pkl".format(trainPlayer,iterNo))
	act.save_act("shannon_switching_train_{}_{}.pkl".format(trainPlayer,iterNo))
	# print("Saving model to shannon_switching.pkl")
	# act.save("shannon_switching.pkl")
	 #x.step([0, 0, 0, 1, 0, 0, 2])[0][0]
if __name__ == '__main__':
	main()



