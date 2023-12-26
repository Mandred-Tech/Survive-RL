import random

from base_envi import Simulation, Herbivore

env = Simulation(2, 10, 10, 10, 100, 100,10, 10, -10, 'random', 2,60)

herbivore_list, carnivore_list, _, _ = env.get_lists()
done = False
# herbi=Herbivore(1,"red",11,0,0)
# herbi.health=500
while not done:
    done, _ = env.step()
    # done, obs = env.step(herbivore_list[0], 1)
    # env.test_move(herbi)
env.stop()
