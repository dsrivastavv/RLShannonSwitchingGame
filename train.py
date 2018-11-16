import gym
import shannon_switching
from baselines import deepq
from baselines.common import models

# def callback(lcl, _glb):
	# stop training if reward exceeds 199
	# is_solved = lcl['t'] > 100 and sum(lcl['episode_rewards'][-101:-1]) / 100 >= 1000
	# # print(lcl)
	# return is_solved
	
def main():
	env = gym.make("shannon_switching-v0")
	act = deepq.learn(
		env,
		network=models.mlp(num_hidden=7, num_layers=1),
		lr=1e-4,
		total_timesteps=50000,
		buffer_size=50000,
		exploration_fraction=0.1,
		exploration_final_eps=1e-10,
		print_freq=1,
		param_noise=False,
	)
	print("Saving model to shannon_switching.pkl")
	act.save("shannon_switching.pkl")

if __name__ == '__main__':
	main()