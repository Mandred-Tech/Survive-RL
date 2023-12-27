# Running Random simulations for n number of times and storing results in csv
from base_envi import Simulation
import pandas as pd

number_of_simulations=10
df=pd.read_csv('random_results.csv')
for i in range(0,number_of_simulations):
    env = Simulation(10, 10, 100, 50, 100, 100, 10, 10, -10, 'random', 2, 60, 50)
    herbivore_list, carnivore_list, _, _ = env.get_lists()
    done = False
    while not done:
        done, obs = env.step()
    dic_res={'Generation':i,'Winner':obs}
    print(dic_res,len(herbivore_list),len(carnivore_list))
    df = df._append(dic_res, ignore_index=True)
    env.stop()
df.to_csv('random_results.csv',index=False)