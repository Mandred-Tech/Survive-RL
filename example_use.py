from base_envi import Simulation

env=Simulation(15,10,15,15,100,100)


done = False
while not done:
    done = env.step()
env.stop()



