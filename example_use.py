import random

from base_envi import Simulation

env = Simulation(10, 10, 60, 15, 100, 100, 'random')

# herbivore_list, _, _, _ = env.step()
done = False
while not done:
    done=env.step()
env.stop()
