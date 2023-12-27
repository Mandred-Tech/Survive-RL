# Running Random simulations for n number of times and storing results in csv
import random

from base_envi import Simulation
import pandas as pd

number_of_simulations = 1
for i in range(0, number_of_simulations):
    env = Simulation(5, 5, 100, 50, 100, 100, 10, 10, -10, 'custom', 1, 30, 50)
    herbivore_list, carnivore_list, _, _ = env.get_lists()
    herbi1, herbi2, herbi3, herbi4, herbi5 = herbivore_list[0], herbivore_list[1], herbivore_list[2], herbivore_list[3], \
                                             herbivore_list[4]
    carni1, carni2, carni3, carni4, carni5 = carnivore_list[0], carnivore_list[1], carnivore_list[2], carnivore_list[3], \
                                             carnivore_list[4]
    done = 0
    while done == 0:
        d1, obs1 = env.step(carni1, 1)
        print("1",d1,obs1)
        d2, obs2 = env.step(carni2, 2)
        print("2",d2, obs2)
        d3, obs3 = env.step(carni3, 3)
        print("3",d3, obs3)
        d4, obs4 = env.step(carni4, 4)
        print("4",d4, obs4)
        d5, obs5 = env.step(carni5, 3)
        print("5",d5, obs5)
        d6, obs6 = env.step(herbi1, 2)
        print("1h", d6, obs6)
        d7, obs7 = env.step(herbi2, 1)
        print("2h", d7, obs7)
        d8, obs8 = env.step(herbi3, 4)
        print("3h", d8, obs8)
        d9, obs9 = env.step(herbi4, 3)
        print("4h", d9, obs9)
        d10, obs10 = env.step(herbi5, 1)
        print("5h", d10, obs10)
        # print(carni1,carni2,carni3,carni4,carni5)
        # print(len(carnivore_list),len(herbivore_list))
        done= d1 and d2 and d3 and d4 and d5 and d6 and d7 and d8 and d9 and d10
    print("Final Done+",done)
    # print(done,obs)
    # print(len(herbivore_list),len(carnivore_list))
    env.stop()
