# Survive-RL
The reinforcement learning environment with advanced interaction between the agents.

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