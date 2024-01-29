![Logo](Logo.png)
# Survive-RL
The reinforcement learning environment with advanced interaction between the agents.
Video Explanation: https://youtu.be/jYEJakEAMzM?si=n_CALfYUGUDMKFSB
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
and the health of each agent is mean of the total health of both agents.(mean= (health1+health2)/2)
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

### How to use it
- Clone this repository in your workspace or just download the files manually.
- Run the random_test.py which shows how to start the simulation for n number of times and storing the result in the csv.
- Run the custom_use_example.py which shows how to run the simulation by specifying the agents movements manually or using any function.
- Run the Genetic_Algo_implementation.py which shows how to run the simulation using a basic genetic algorithm.
- More details about the functions, calls and references can be found in the base_envi.py script which is the main environment code running on pygame.

##MIT License with Attribution

Copyright (c) [2024] [Mandred Tech]

Permission is hereby granted, free of charge, to any person obtaining a copy of this software and associated documentation files (the "Software"), to deal in the Software without restriction, including without limitation the rights to use, copy, modify, merge, publish, distribute, sublicense, and/or sell copies of the Software, and to permit persons to whom the Software is furnished to do so, subject to the following conditions:

The above copyright notice and this permission notice shall be included in all copies or substantial portions of the Software.

**Attribution Clause:**
Users of this software are required to include an attribution to Mandred Tech in any publication, distribution, or derivative works based on this software.

THE SOFTWARE IS PROVIDED "AS IS", WITHOUT WARRANTY OF ANY KIND, EXPRESS OR IMPLIED, INCLUDING BUT NOT LIMITED TO THE WARRANTIES OF MERCHANTABILITY, FITNESS FOR A PARTICULAR PURPOSE AND NONINFRINGEMENT. IN NO EVENT SHALL THE AUTHORS OR COPYRIGHT HOLDERS BE LIABLE FOR ANY CLAIM, DAMAGES OR OTHER LIABILITY, WHETHER IN AN ACTION OF CONTRACT, TORT OR OTHERWISE, ARISING FROM, OUT OF OR IN CONNECTION WITH THE SOFTWARE OR THE USE OR OTHER DEALINGS IN THE SOFTWARE.

