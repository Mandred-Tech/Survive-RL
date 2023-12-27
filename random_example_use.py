import random

from base_envi import Simulation

env = Simulation(100, 1, 10, 100, 100, 100,10, 10, -10, 'custom', 2,6,15)

herbivore_list, carnivore_list, _, _ = env.get_lists()
# herbi_inx=[i.id for i in herbivore_list]
# print(len(herbivore_list))
done = False
# herbi=Herbivore(1,"red",11,0,0)
# herbi.health=500
while not done:
    # done, obs = env.step()
    # print(done,obs)
    # herbivore_list, carnivore_list, _, _ = env.get_lists()
    # print(len(herbivore_list))
    done, obs = env.step(herbivore_list[0], 1)
    # print(herbivore_list)
    print(done, obs)
    # env.test_move(herbi_list[0])
    # print(len(herbi_list))
env.stop()
