# Setups for setting up environment
```  
import gym
import shannon_switching
env = gym.make('shannon_switching-v0')
```

# Notes
1. After changing any files in this directory or its subdirectories re-install the package

# References
1. Getting started with [Gym](https://gym.openai.com/docs/)
2. Description of `Env` class could be found [here](https://github.com/openai/gym/blob/master/gym/core.py)
3. An example implementation could be found [here](https://github.com/openai/gym/blob/master/gym/envs/classic_control/mountain_car.py)
4. What is `observation space`? Description could be found [here](https://github.com/openai/gym/issues/593)
5. Steps to overload gym class can be found [here](https://stackoverflow.com/questions/44469266/how-to-implement-custom-environment-in-keras-rl-openai-gym)
6. DQN [Example](https://github.com/openai/baselines/blob/master/baselines/deepq/experiments/train_mountaincar.py)
