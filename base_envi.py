""" 1 for Herbivore, 2 for Carnivore, 3 for Plants, 4 for Rocks"""
""" 1 for up direction, 2 for down direction, 3 for left, 4 for right"""
"""Simulation_controller variable is "custom" if user wants to use his own NN or function, "random" for random 
actions """
import pygame
from config import colors, fonts
import random
from itertools import product
import math

""" Class for handling the game environment and the agents playing the game."""

class Environment:  
    def __init__(self, number_of_herbivores, number_of_carnivores, number_of_plants, number_of_rocks,
                 health_herbivore, health_carnivore):
        self.number_of_herbivores = number_of_herbivores
        self.number_of_carnivores = number_of_carnivores
        self.health_herbivore = health_herbivore
        self.health_carnivore = health_carnivore
        self.number_of_plants = number_of_plants
        self.number_of_rocks = number_of_rocks
        self.size_of_tile = 25
        self.window_width = 1500
        self.window_height = 600
        self.number_of_rows = self.window_height // self.size_of_tile
        self.number_of_columns = self.window_width // self.size_of_tile
        self.user_steps = user_steps

    def background_tile_map_layer(self, display_surface): # Function for initializing the 3 tile maps.
        background_tile_map = [[0] * self.number_of_columns for i in range(0, self.number_of_rows)]
        agent_tile_map = [[0] * self.number_of_columns for i in range(0, self.number_of_rows)]
        obstacle_tile_map = [[0] * self.number_of_columns for i in range(0, self.number_of_rows)]
        for row in range(0, len(background_tile_map)):
            for column in range(0, len(background_tile_map[0])):
                rect = pygame.draw.rect(display_surface, colors('light_blue'),
                                        (column * self.size_of_tile, (row * self.size_of_tile) + 50,
                                         self.size_of_tile - 1, self.size_of_tile - 1), 2)
                background_tile_map[row][column] = pygame.Rect(rect)
        return background_tile_map, agent_tile_map, obstacle_tile_map

    def environment_setter(self): # For creating the agents and obstacles and initializing the item buffer lists.
        total_randoms = self.number_of_carnivores + self.number_of_herbivores + self.number_of_plants + self.number_of_rocks
        sample_combinations = list(product(list(range(0, self.number_of_rows)), list(range(0, self.number_of_columns))))
        required_sample = random.sample(sample_combinations, total_randoms)
        herbivore_list = []
        carnivore_list = []
        plant_list = []
        rock_list = []
        for i in range(0, self.number_of_herbivores):
            herbivore_list.append(
                Herbivore(i, herbivore_color, self.health_herbivore, required_sample[i][0], required_sample[i][1]))
        for i in range(self.number_of_herbivores, self.number_of_herbivores + self.number_of_plants):
            plant_list.append(Plant(i, plant_color, plant_value, required_sample[i][0], required_sample[i][1]))
        for i in range(self.number_of_herbivores + self.number_of_plants,
                       self.number_of_herbivores + self.number_of_plants + self.number_of_rocks):
            rock_list.append(Rock(i, rock_color, rock_value, required_sample[i][0], required_sample[i][1]))
        for i in range(self.number_of_rocks + self.number_of_plants + self.number_of_herbivores,
                       self.number_of_carnivores + self.number_of_plants + self.number_of_rocks + self.number_of_herbivores):
            carnivore_list.append(
                Carnivore(i, carnivore_color, self.health_carnivore, required_sample[i][0], required_sample[i][1]))

        return herbivore_list, carnivore_list, plant_list, rock_list

    def step(self, agent=None, action=None): # For incrementing the game by one time step. Moving all agents once will conclude one global step.

        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                return True, None

        herbivore_health_txt, herbivore_health_txt_rect = fonts('font2', 25,
                                                                "Herbivore Health : " + str(mean_population_health(herbivore_list)),
                                                                (600, 25), colors('white'))
        carnivore_health_txt, carnivore_health_txt_rect = fonts('font2', 25,
                                                                "Carnivore Health : " + str(mean_population_health(carnivore_list)),
                                                                (1200, 25), colors('white'))
        pygame.draw.rect(display_surface, colors('blue_green'), (0,0,2000,50))
        pygame.draw.rect(display_surface, colors('blue_green'), (0, 650, 2000, 800))
        display_surface.blit(title_txt, title_txt_rect)
        display_surface.blit(company_txt, company_txt_rect)
        display_surface.blit(herbivore_health_txt, herbivore_health_txt_rect)
        display_surface.blit(carnivore_health_txt, carnivore_health_txt_rect)
        match simulation_controller:
            case 'random':
                self.user_steps -= 1
                self.random_move(herbivore_list)
                self.random_move(carnivore_list)
                a, b = game_master(self.user_steps)
                if a == True:
                    return True, b
            case 'custom':
                if agent == None:
                    return True, "No agent"
                self.user_steps -= 1 / (self.number_of_herbivores + self.number_of_carnivores)
                a, b = game_master(self.user_steps)
                if a == True:
                    return True, b
                ob = agent.move(action)
                if ob != 'Dead':
                    return False, ob
                else:
                    return True, ob
            case _:
                print("Wrong Simulation controller. Please check!")
                return True, None

        return False, None

    def stop(self): # For exiting out of the game loop.
        pygame.quit()
        return True

    def random_move(self, agent_list): # For randomly moving the agents. Note: Don't use it separately it will be used when the simulation controller is 'random'
        for i in agent_list[0:len(agent_list) - 1]:
            i.move(random.randint(1, 4))

    def test_move(self, agent):  # For manually moving a particular agent. Note: This was used for debugging not for actual use in environment.
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                running = False
            if event.type == pygame.KEYDOWN:
                if event.key == pygame.K_UP:
                    print(agent.move(1))
                if event.key == pygame.K_DOWN:
                    print(agent.move(2))
                if event.key == pygame.K_LEFT:
                    print(agent.move(3))
                if event.key == pygame.K_RIGHT:
                    print(agent.move(4))

        display_surface.blit(title_txt, title_txt_rect)
        display_surface.blit(company_txt, company_txt_rect)
        pygame.display.update()
        clock.tick(FPS)

    def get_lists(self): # Returns the 4 lists initialized with the objects. Note: None has been added as a check so only len(list)-2 indices to be used.
        global herbivore_list, carnivore_list, plant_list, rock_list
        herbivore_list.append(None)
        carnivore_list.append(None)
        return herbivore_list, carnivore_list, plant_list, rock_list

""" Class for initializing the herbivore agent and handles its movement and other functions."""

class Herbivore:
    def __init__(self, identifier, color, health, row_number, column_number):
        self.name = 'h'
        self.id = identifier
        self.color = color
        self.health = health
        self.row_number = row_number
        self.column_number = column_number
        self.storage = [0]
        self.herbivore_steps = 0
        pygame.draw.rect(display_surface, colors(self.color), back_tile_map[row_number][column_number])
        agent_tile_map[row_number][column_number] = 1

    def move(self, direction): # Function to move the herbivore agent according to the action provided.
        if self.id not in [i.id for i in herbivore_list[-2::-1]]:
            return "Dead"
        self.herbivore_steps += 1
        prev_row = self.row_number
        prev_col = self.column_number
        mover = [0, 0]  # variable to find what was the previous move of the agent
        match direction:
            case 1:
                self.row_number -= 1
                self.row_number = row_checker(self.row_number)
                mover = [-1, 0]
            case 2:
                self.row_number += 1
                self.row_number = row_checker(self.row_number)
                mover = [1, 0]
            case 4:
                self.column_number += 1
                self.column_number = column_checker(self.column_number)
                mover = [0, 1]
            case 3:
                self.column_number -= 1
                self.column_number = column_checker(self.column_number)
                mover = [0, -1]
        # Checking the new location for herbivore to swap the agents.
        if agent_tile_map[self.row_number][self.column_number] == 1:
            agent_tile_map[prev_row][prev_col] = 1
            swapped_herbivore = object_finder(self.id, herbivore_list, self.row_number, self.column_number)
            swapped_herbivore.row_number = prev_row
            swapped_herbivore.column_number = prev_col
            mean_health(self, swapped_herbivore)

        # Removing the herbivore if the new location is the carnivore.
        elif agent_tile_map[self.row_number][self.column_number] == 2 and obstacle_tile_map[self.row_number][
            self.column_number] == 0:
            carnivore_obj = object_finder(-1, carnivore_list, self.row_number, self.column_number)
            carnivore_obj.health += herbivore_value
            herbivore_list.remove(self)
            agent_tile_map[prev_row][prev_col] = 0

        # Moving rocks in this function instead of updater
        elif obstacle_tile_map[self.row_number][self.column_number] == 4:
            self.health += rock_value
            rock_obj = object_finder(-1, rock_list, self.row_number, self.column_number)
            new_rock_row = self.row_number + mover[0]
            new_rock_row = row_checker(new_rock_row)
            new_rock_col = self.column_number + mover[1]
            new_rock_col = column_checker(new_rock_col)
            if obstacle_tile_map[new_rock_row][new_rock_col] == 3:  # checking for plant on push
                plant_obj = object_finder(-1, plant_list, new_rock_row, new_rock_col)
                plant_list.remove(plant_obj)
            if obstacle_tile_map[new_rock_row][new_rock_col] == 4:  # checking for rock on push
                ro_obj = object_finder(-1, rock_list, new_rock_row, new_rock_col)
                rock_list.remove(ro_obj)
            obstacle_tile_map[new_rock_row][new_rock_col] = 4
            obstacle_tile_map[self.row_number][self.column_number] = 0
            agent_tile_map[self.row_number][self.column_number] = 1
            agent_tile_map[prev_row][prev_col] = 0
            rock_obj.row_number = new_rock_row
            rock_obj.column_number = new_rock_col

        else:
            agent_tile_map[prev_row][prev_col] = 0
            agent_tile_map[self.row_number][self.column_number] = 1
        updater()
        dead = self.health_check()
        if simulation_controller != "random" and dead != 0:
            return self.observation_space()
        else:
            return "Dead"

    def observation_space(self): # Provides the nearby grids as the agent moves.
        min_row = min(self.row_number - observation_space,
                      self.row_number + observation_space)
        max_row = max(self.row_number - observation_space,
                      self.row_number + observation_space)
        min_column = min(self.column_number - observation_space,
                         self.column_number + observation_space)
        max_column = max(self.column_number - observation_space,
                         self.column_number + observation_space)
        observation_rows = list(range(min_row, max_row + 1))
        observation_columns = list(range(min_column, max_column + 1))
        required_space = list(product(observation_rows, observation_columns))
        required_space.remove((self.row_number, self.column_number))
        temp_space_list = []
        for i in required_space:
            row = row_checker(i[0])
            column = column_checker(i[1])
            temp_space_list.append(agent_tile_map[row][column] + obstacle_tile_map[row][column])
        temp_space_list.append(self.health)  # adding health to output to send
        temp_space_list.append(self.herbivore_steps)
        return temp_space_list

    def health_check(self): # Checking the agent health and removing the agent if health falls below zero.
        if self.health <= 0:
            if self.id in [i.id for i in herbivore_list[-2::-1]]:
                herbivore_list.remove(self)
            agent_tile_map[self.row_number][self.column_number] = 0
            return 0
        else:
            return 1

""" Class for initializing the carnivore agent and handles its movement and other functions. Functions similar to herbivore."""
class Carnivore:
    def __init__(self, identifier, color, health, row_number, column_number):
        self.name = 'c'
        self.id = identifier
        self.color = color
        self.health = health
        self.row_number = row_number
        self.column_number = column_number
        self.storage = [0]
        self.carnivore_steps = 0
        pygame.draw.rect(display_surface, colors(self.color), back_tile_map[row_number][column_number])
        agent_tile_map[row_number][column_number] = 2

    def move(self, direction):
        if self.id not in [i.id for i in carnivore_list[-2::-1]]:
            return "Dead"
        self.carnivore_steps += 1
        prev_row = self.row_number
        prev_col = self.column_number
        mover = [0, 0]  # variable to find what was the previous move of the agent
        match direction:
            case 1:
                self.row_number -= 1
                self.row_number = row_checker(self.row_number)
                mover = [-1, 0]
            case 2:
                self.row_number += 1
                self.row_number = row_checker(self.row_number)
                mover = [1, 0]
            case 4:
                self.column_number += 1
                self.column_number = column_checker(self.column_number)
                mover = [0, 1]
            case 3:
                self.column_number -= 1
                self.column_number = column_checker(self.column_number)
                mover = [0, -1]

        if agent_tile_map[self.row_number][self.column_number] == 2:
            agent_tile_map[prev_row][prev_col] = 2
            swapped_carnivore = object_finder(self.id, carnivore_list, self.row_number, self.column_number)
            swapped_carnivore.row_number = prev_row
            swapped_carnivore.column_number = prev_col
            mean_health(self, swapped_carnivore)

        # Removing herbivore if carnivore moves to its location.
        elif agent_tile_map[self.row_number][self.column_number] == 1 and obstacle_tile_map[self.row_number][
            self.column_number] == 0:
            herbivore_obj = object_finder(-1, herbivore_list, self.row_number, self.column_number)
            self.health += herbivore_value
            herbivore_list.remove(herbivore_obj)
            agent_tile_map[prev_row][prev_col] = 0
            agent_tile_map[self.row_number][self.column_number] = 2

        # Moving rocks in this function instead of updater
        elif obstacle_tile_map[self.row_number][self.column_number] == 4:
            self.health += rock_value
            rock_obj = object_finder(-1, rock_list, self.row_number, self.column_number)
            new_rock_row = self.row_number + mover[0]
            new_rock_row = row_checker(new_rock_row)
            new_rock_col = self.column_number + mover[1]
            new_rock_col = column_checker(new_rock_col)
            if obstacle_tile_map[new_rock_row][new_rock_col] == 3:  # checking for plant on push
                plant_obj = object_finder(-1, plant_list, new_rock_row, new_rock_col)
                plant_list.remove(plant_obj)
            if obstacle_tile_map[new_rock_row][new_rock_col] == 4:  # checking for rock on push
                ro_obj = object_finder(-1, rock_list, new_rock_row, new_rock_col)
                rock_list.remove(ro_obj)
            obstacle_tile_map[new_rock_row][new_rock_col] = 4
            obstacle_tile_map[self.row_number][self.column_number] = 0
            agent_tile_map[self.row_number][self.column_number] = 2
            agent_tile_map[prev_row][prev_col] = 0
            rock_obj.row_number = new_rock_row
            rock_obj.column_number = new_rock_col

        else:
            agent_tile_map[prev_row][prev_col] = 0
            agent_tile_map[self.row_number][self.column_number] = 2
        updater()
        dead = self.health_check()
        if simulation_controller != "random" and dead != 0:
            return self.observation_space()
        else:
            return "Dead"

    def observation_space(self):
        min_row = min(self.row_number - observation_space,
                      self.row_number + observation_space)
        max_row = max(self.row_number - observation_space,
                      self.row_number + observation_space)
        min_column = min(self.column_number - observation_space,
                         self.column_number + observation_space)
        max_column = max(self.column_number - observation_space,
                         self.column_number + observation_space)
        observation_rows = list(range(min_row, max_row + 1))
        observation_columns = list(range(min_column, max_column + 1))
        required_space = list(product(observation_rows, observation_columns))
        required_space.remove((self.row_number, self.column_number))
        temp_space_list = []
        for i in required_space:
            row = row_checker(i[0])
            column = column_checker(i[1])
            temp_space_list.append(agent_tile_map[row][column] + obstacle_tile_map[row][column])
        temp_space_list.append(self.health)  # adding health to output to send
        temp_space_list.append(self.carnivore_steps)
        return temp_space_list

    def health_check(self):
        if self.health <= 0:
            if self.id in [i.id for i in carnivore_list[-2::-1]]:
                carnivore_list.remove(self)
            agent_tile_map[self.row_number][self.column_number] = 0
            return 0
        else:
            return 1

"""Class for creating a plant object."""
class Plant:
    def __init__(self, identifier, color, value, row_number, column_number):
        self.id = identifier
        self.color = color
        self.reward_value = value
        self.row_number = row_number
        self.column_number = column_number
        pygame.draw.rect(display_surface, colors(self.color), back_tile_map[row_number][column_number], 5)
        obstacle_tile_map[row_number][column_number] = 3

"""Class for creating a rock object."""
class Rock:
    def __init__(self, identifier, color, value, row_number, column_number):
        self.id = identifier
        self.color = color
        self.reward_value = value
        self.row_number = row_number
        self.column_number = column_number
        pygame.draw.rect(display_surface, colors(self.color), back_tile_map[row_number][column_number], 8)
        obstacle_tile_map[row_number][column_number] = 4


def mean_health(agent1, agent2): # Calculating the mean health on swapping of the similar agents.
    mean_health = (math.ceil(agent1.health + agent2.health) / 2)
    agent1.health = int(mean_health)
    agent2.health = int(mean_health)


def row_checker(row_number): # To check if the new row is not beyond the limit.
    if row_number < 0:
        row_number = len(agent_tile_map) - 1
    if row_number > len(agent_tile_map) - 1:
        row_number = 0
    return row_number


def column_checker(column_number): # To check if the new column is not beyond the limit.
    if column_number < 0:
        column_number = len(agent_tile_map[0]) - 1
    if column_number > len(agent_tile_map[0]) - 1:
        column_number = 0
    return column_number


def updater():  # This function can be called whenever entire environment has to be changed based on changes in tile-map
    for row in range(0, len(back_tile_map)):
        for column in range(0, len(back_tile_map[0])):
            pygame.draw.rect(display_surface, colors('grey'), back_tile_map[row][column])
            pygame.draw.rect(display_surface, colors('light_blue'),
                             back_tile_map[row][column], 2)
            if agent_tile_map[row][column] == 1 and obstacle_tile_map[row][column] == 0: # For drawing the herbivore
                pygame.draw.rect(display_surface, colors(herbivore_color), back_tile_map[row][column])
            elif agent_tile_map[row][column] == 1 and obstacle_tile_map[row][column] == 3: # Plant and herbivore interaction
                pygame.draw.rect(display_surface, colors(herbivore_color), back_tile_map[row][column])
                plant_obj = object_finder(-1, plant_list, row, column)
                object_finder(-1, herbivore_list, row, column).health += plant_obj.reward_value
                plant_list.remove(plant_obj)
                obstacle_tile_map[row][column] = 0
            elif agent_tile_map[row][column] == 1 and obstacle_tile_map[row][column] == 4: # Rock and herbivore interaction
                herbi_obj = object_finder(-1, herbivore_list, row, column)
                herbivore_list.remove(herbi_obj)
                agent_tile_map[row][column] = 0
                pygame.draw.rect(display_surface, colors(rock_color), back_tile_map[row][column], 8)
                
            elif agent_tile_map[row][column] == 0 and obstacle_tile_map[row][column] == 3: # Plant drawing
                pygame.draw.rect(display_surface, colors(plant_color), back_tile_map[row][column], 5)

            elif agent_tile_map[row][column] == 0 and obstacle_tile_map[row][column] == 4: # Rock drawing
                pygame.draw.rect(display_surface, colors(rock_color), back_tile_map[row][column], 8)
                
            elif agent_tile_map[row][column] == 2 and obstacle_tile_map[row][column] == 0:  # Carnivore drawing
                pygame.draw.rect(display_surface, colors(carnivore_color), back_tile_map[row][column])

            elif agent_tile_map[row][column] == 2 and obstacle_tile_map[row][
                column] == 3:  # Carnivore and plant interaction
                pygame.draw.rect(display_surface, colors(carnivore_color), back_tile_map[row][column])
                plant_obj = object_finder(-1, plant_list, row, column)
                object_finder(-1, carnivore_list, row, column).health -= plant_obj.reward_value
                plant_list.remove(plant_obj)
                obstacle_tile_map[row][column] = 0
                    
            elif agent_tile_map[row][column] == 2 and obstacle_tile_map[row][
                column] == 4:  # Carnivore and rock interaction
                carni_obj = object_finder(-1, carnivore_list, row, column)
                carnivore_list.remove(carni_obj)
                agent_tile_map[row][column] = 0
                pygame.draw.rect(display_surface, colors(rock_color), back_tile_map[row][column], 8)

    pygame.display.update()
    clock.tick(FPS)


def object_finder(idx_avoid, object_list, row, column): # To find the object given the list and location.
    for i in object_list:
        if i.row_number == row and i.column_number == column and i.id != idx_avoid:
            return i
    return None


def game_master(user_st): # To check for the game overs depending on the steps user specified or the len of the agent lists.
    if user_st <= 1:
        if len(herbivore_list) > len(carnivore_list):
            return True, "Herbivore Wins"
        elif len(herbivore_list) < len(carnivore_list):
            return True, "Carnivore Wins"
        elif len(herbivore_list) == len(carnivore_list):
            if mean_population_health(herbivore_list)>mean_population_health(carnivore_list):
                return True, "Herbivore Wins"
            elif mean_population_health(herbivore_list)<mean_population_health(carnivore_list):
                return True, "Carnivore Wins"
            else:
                return True, "Herbivore Wins" # After all these cases if again mean health same then herbivore winner
                # by default
    else:
        if len(herbivore_list) == 1:
            return True, "Carnivore Wins"

        elif len(carnivore_list) == 1:
            return True, "Herbivore Wins"
        else:
            return False, None


def mean_population_health(agent_list): # Returns the mean health of the entire agent population separately.
    s = 0
    for i in agent_list[-2::-1]:
        s += i.health
    if len(agent_list)-1!=0:
        mean_pop=s//(len(agent_list)-1)
    else:
        mean_pop=0
    return mean_pop


def Simulation(number_of_herbivores, number_of_carnivores, number_of_plants, number_of_rocks,
               health_herbivore, health_carnivore, herbivore_reward=15, plant_reward=10, rock_reward=-2,
               sim_controller='random',
               obs_space=1, speed=30, available_steps=200): # Function to handle calls from external script.
    pygame.init()
    global WINDOW_WIDTH
    global WINDOW_HEIGHT
    WINDOW_WIDTH = 1500
    WINDOW_HEIGHT = 700
    global display_surface
    display_surface = pygame.display.set_mode((WINDOW_WIDTH, WINDOW_HEIGHT))
    display_surface.fill(colors('grey'))
    pygame.display.set_caption("SURVIVE RL")
    global herbivore_color
    global carnivore_color
    global plant_color
    global rock_color
    herbivore_color = 'blue'
    carnivore_color = 'red'
    plant_color = 'green'
    rock_color = 'black'
    global plant_value
    global rock_value
    global herbivore_value
    plant_value = plant_reward
    rock_value = rock_reward
    herbivore_value = herbivore_reward
    global user_steps
    user_steps = available_steps
    global FPS
    global clock
    FPS = speed
    clock = pygame.time.Clock()

    global title_txt
    global title_txt_rect
    global company_txt
    global company_txt_rect
    global herbivore_health_txt
    global herbivore_health_txt_rect
    global carnivore_health_txt
    global carnivore_health_txt_rect
    title_txt, title_txt_rect = fonts('font3', 40, "Survive RL", (100, 25), colors('light_green'))
    company_txt, company_txt_rect = fonts('font3', 40, "Mandred Tech", (1375, 680), colors('light_red'))
    herbivore_health_txt, herbivore_health_txt_rect = fonts('font2', 25, "Herbivore Health : "+str(health_herbivore), (600, 25), colors('white'))
    carnivore_health_txt, carnivore_health_txt_rect = fonts('font2', 25, "Carnivore Health : "+str(health_carnivore), (1200, 25), colors('white'))
    envi = Environment(number_of_herbivores, number_of_carnivores, number_of_plants, number_of_rocks,
                       health_herbivore, health_carnivore)
    global back_tile_map
    global agent_tile_map
    global obstacle_tile_map
    global herbivore_list
    global carnivore_list
    global rock_list
    global plant_list
    back_tile_map, agent_tile_map, obstacle_tile_map = envi.background_tile_map_layer(display_surface)
    herbivore_list, carnivore_list, plant_list, rock_list = envi.environment_setter()
    global simulation_controller
    simulation_controller = sim_controller
    global observation_space
    observation_space = obs_space
    return envi


print("WELCOME TO SURVIVE_RL")
print("MANDRED TECH 🚀 - MIT LICENCE")
print("Number of Rows : 24   Number of Columns : 60")
print()
