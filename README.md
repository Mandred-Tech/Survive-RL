![What is this](Logo.png)
# Survive-RL
The reinforcement learning environment with advanced interaction between the agents.

### Interactions
The following interactions take place:
1. When agent tries to move into the block of the rock,the rock moves
in the same direction in which agent tries to move. This move
costs health (default -2 loss in health)
2. When herbivore moves on plant block, the plant is removed and 
herbivore agent gets a reward (default +10 gain in health)
3. When carnivore moves on plant block, the plant is removed and 
carnivore agent gets a negative reward (default -10 loss in health)
4. When a rock is pushed on another block containing rock, then one rock is removed
from the environment and one rock is left.
5. When rock is pushed on another block containing plant, then the plant is removed
from the environment and rock is left.
6. When an agent tries to move to another similar agent block, then they swap their locations
and the health of each agent is mean of the total health of both agents.(health meaning is not yet implemented)
7. When Herbivore tries to move to carnivore position or vice versa, the herbivore is
removed from the environment and carnivore gains a reward.(default is +10 gain in health)


### Action Space
The action space of each agent is:
1. To move up
2. To move down
3. To move left
4. To move right

### Observations
The output of each step is:
- (n+(n-1)+(n-2)+....1) * 8 where n is the value of obs_space variable
in Simulation function. Its default value is 1.

### Check the random_test.py for running the simulation for n number of times and storing in the csv.
### Check the custom_use_example.py for running the simulation by specifying the agents movements.
