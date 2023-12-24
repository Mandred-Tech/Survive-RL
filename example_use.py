import random

from base_envi import Simulation,Herbivore

env = Simulation(10, 1, 1, 1, 100, 100,10,-1, 'custom', 2)

herbivore_list, _, _, _ = env.get_lists()
done = False
# Herbivore(1,"red",11,0,0)
while not done:
    # done, obs = env.step(herbivore_list[0], 1)
    env.test_move(herbivore_list[0])
env.stop()
