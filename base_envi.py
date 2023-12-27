""" 1 for Herbivore 2 for Carnivore 3 for Plants 4 for Rocks"""
""" 1 for up direction 2 for down direction 3 for left and 4 for right"""
"""simulation_controller variable is "custom" if user wants to use his own NN or function, "random" for random 
actions """
import pygame
from config import colors, fonts
import random
from itertools import product
import math


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
        print(self.number_of_rows, self.number_of_columns)

    def background_tile_map_layer(self, display_surface):
        background_tile_map = [[0] * self.number_of_columns for i in range(0, self.number_of_rows)]
        agent_tile_map = [[0] * self.number_of_columns for i in range(0, self.number_of_rows)]
        obstacle_tile_map = [[0] * self.number_of_columns for i in range(0, self.number_of_rows)]
        # print(len(background_tile_map), len(background_tile_map[0]))
        for row in range(0, len(background_tile_map)):
            for column in range(0, len(background_tile_map[0])):
                rect = pygame.draw.rect(display_surface, colors('light_blue'),
                                        (column * self.size_of_tile, (row * self.size_of_tile) + 50,
                                         self.size_of_tile - 1, self.size_of_tile - 1), 2)
                background_tile_map[row][column] = pygame.Rect(rect)
        return background_tile_map, agent_tile_map, obstacle_tile_map

    def environment_setter(self):
        total_randoms = self.number_of_carnivores + self.number_of_herbivores + self.number_of_plants + self.number_of_rocks
        sample_combinations = list(product(list(range(0, self.number_of_rows)), list(range(0, self.number_of_columns))))
        required_sample = random.sample(sample_combinations, total_randoms)
        # print(required_sample)
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

    def step(self, agent=None, action=None):
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                return True, None
        display_surface.blit(title_txt, title_txt_rect)
        display_surface.blit(company_txt, company_txt_rect)
        match simulation_controller:
            case 'random':
                self.random_move(herbivore_list)
                self.random_move(carnivore_list)
            case 'custom':
                obs = agent.move(action)
                if obs is not None:
                    return False, obs
                else:
                    return True, observation_list_length()
            case _:
                print("Wrong Simulation controller. Please check!")
                return True, None
        return False, None

    def stop(self):
        pygame.quit()
        return True

    def random_move(self, agent_list):
        for i in agent_list:
            i.move(random.randint(1, 4))

    def test_move(self, agent):  # for manually moving a particular agent
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                running = False
            if event.type == pygame.KEYDOWN:
                if event.key == pygame.K_UP:
                    print(self.step(agent,1))
                if event.key == pygame.K_DOWN:
                    print(self.step(agent,2))
                if event.key == pygame.K_LEFT:
                    print(self.step(agent,3))
                if event.key == pygame.K_RIGHT:
                    print(self.step(agent,4))

        display_surface.blit(title_txt, title_txt_rect)
        display_surface.blit(company_txt, company_txt_rect)
        pygame.display.update()
        clock.tick(FPS)

    def get_lists(self):
        global herbivore_list, carnivore_list, plant_list, rock_list
        return herbivore_list, carnivore_list, plant_list, rock_list


class Herbivore:
    def __init__(self, identifier, color, health, row_number, column_number):
        self.id = identifier
        self.color = color
        self.health = health
        self.row_number = row_number
        self.column_number = column_number
        self.storage = [0]
        pygame.draw.rect(display_surface, colors(self.color), back_tile_map[row_number][column_number])
        agent_tile_map[row_number][column_number] = 1

    def move(self, direction):
        prev_row = self.row_number
        prev_col = self.column_number
        mover = [0, 0]  # variable to find what was the previous move of the agent
        # print(self.row_number,self.column_number)
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
        # print(self.row_number, self.column_number)
        if agent_tile_map[self.row_number][self.column_number] == 1:
            agent_tile_map[prev_row][prev_col] = 1
            swapped_herbivore = object_finder(self.id, herbivore_list, self.row_number, self.column_number)
            # print(swapped_herbivore.row_number, swapped_herbivore.column_number)
            # print(self.row_number,self.column_number)
            swapped_herbivore.row_number = prev_row
            swapped_herbivore.column_number = prev_col
            mean_health(self, swapped_herbivore)

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
                # print(len(plant_list))
            if obstacle_tile_map[new_rock_row][new_rock_col] == 4:  # checking for rock on push
                ro_obj = object_finder(-1, rock_list, new_rock_row, new_rock_col)
                rock_list.remove(ro_obj)
                # print(len(rock_list))
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
        updater()
        if simulation_controller != "random" and dead != 0:
            return self.observation_space_finder()
        else:
            return None
        # print(agent_tile_map[self.row_number][self.column_number],agent_tile_map[prev_row][prev_col])
        # print(obstacle_tile_map[self.row_number][self.column_number],obstacle_tile_map[prev_row][prev_col])

    def observation_space_finder(self):
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
        # print(self.row_number, self.column_number)
        # print(required_space)
        temp_space_list = []
        for i in required_space:
            row = row_checker(i[0])
            column = column_checker(i[1])
            temp_space_list.append(agent_tile_map[row][column] + obstacle_tile_map[row][column])
        # print(temp_space_list)
        temp_space_list.append(self.health)  # adding health to output to send
        return temp_space_list

    def health_check(self):
        # print(self.health)
        if self.health <= 0:
            herbivore_list.remove(self)
            agent_tile_map[self.row_number][self.column_number] = 0
            return 0
        else:
            return 1


class Carnivore:
    def __init__(self, identifier, color, health, row_number, column_number):
        self.id = identifier
        self.color = color
        self.health = health
        self.row_number = row_number
        self.column_number = column_number
        self.storage = [0]
        pygame.draw.rect(display_surface, colors(self.color), back_tile_map[row_number][column_number])
        agent_tile_map[row_number][column_number] = 2

    def move(self, direction):
        prev_row = self.row_number
        prev_col = self.column_number
        mover = [0, 0]  # variable to find what was the previous move of the agent
        # print(self.row_number,self.column_number)
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
        # print(self.row_number, self.column_number)
        if agent_tile_map[self.row_number][self.column_number] == 2:
            agent_tile_map[prev_row][prev_col] = 2
            swapped_carnivore = object_finder(self.id, carnivore_list, self.row_number, self.column_number)
            # print(swapped_carnivore.row_number, swapped_carnivore.column_number)
            # print(self.row_number,self.column_number)
            swapped_carnivore.row_number = prev_row
            swapped_carnivore.column_number = prev_col
            mean_health(self, swapped_carnivore)

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
                # print(len(plant_list))
            if obstacle_tile_map[new_rock_row][new_rock_col] == 4:  # checking for rock on push
                ro_obj = object_finder(-1, rock_list, new_rock_row, new_rock_col)
                rock_list.remove(ro_obj)
                # print(len(rock_list))
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
        updater()
        if simulation_controller != "random" and dead != 0:
            return self.observation_space_finder()
        else:
            return None
        # print(agent_tile_map[self.row_number][self.column_number],agent_tile_map[prev_row][prev_col])
        # print(obstacle_tile_map[self.row_number][self.column_number],obstacle_tile_map[prev_row][prev_col])

    def observation_space_finder(self):
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
        # print(self.row_number, self.column_number)
        # print(required_space)
        temp_space_list = []
        for i in required_space:
            row = row_checker(i[0])
            column = column_checker(i[1])
            temp_space_list.append(agent_tile_map[row][column] + obstacle_tile_map[row][column])
        # print(temp_space_list)
        temp_space_list.append(self.health)  # adding health to output to send
        return temp_space_list

    def health_check(self):
        # print(self.health)
        if self.health <= 0:
            carnivore_list.remove(self)
            agent_tile_map[self.row_number][self.column_number] = 0
            return 0
        else:
            return 1


class Plant:
    def __init__(self, identifier, color, value, row_number, column_number):
        self.id = identifier
        self.color = color
        self.reward_value = value
        self.row_number = row_number
        self.column_number = column_number
        pygame.draw.rect(display_surface, colors(self.color), back_tile_map[row_number][column_number], 5)
        obstacle_tile_map[row_number][column_number] = 3


class Rock:
    def __init__(self, identifier, color, value, row_number, column_number):
        self.id = identifier
        self.color = color
        self.reward_value = value
        self.row_number = row_number
        self.column_number = column_number
        pygame.draw.rect(display_surface, colors(self.color), back_tile_map[row_number][column_number], 8)
        obstacle_tile_map[row_number][column_number] = 4


def mean_health(agent1, agent2):
    mean_health = math.ceil((agent1.health + agent2.health) / 2)
    agent1.health = mean_health
    agent2.health = mean_health


def row_checker(row_number):
    if row_number < 0:
        row_number = len(agent_tile_map) - 1
    if row_number > len(agent_tile_map) - 1:
        row_number = 0
    return row_number


def column_checker(column_number):
    if column_number < 0:
        column_number = len(agent_tile_map[0]) - 1
    if column_number > len(agent_tile_map[0]) - 1:
        column_number = 0
    return column_number


def updater():  # this function can be called whenever entire environment has to be changed based on changes in tile-map
    for row in range(0, len(back_tile_map)):
        for column in range(0, len(back_tile_map[0])):
            pygame.draw.rect(display_surface, colors('grey'), back_tile_map[row][column])
            pygame.draw.rect(display_surface, colors('light_blue'),
                             back_tile_map[row][column], 2)
            if agent_tile_map[row][column] == 1 and obstacle_tile_map[row][column] == 0:
                pygame.draw.rect(display_surface, colors(herbivore_color), back_tile_map[row][column])
            elif agent_tile_map[row][column] == 1 and obstacle_tile_map[row][column] == 3:
                pygame.draw.rect(display_surface, colors(herbivore_color), back_tile_map[row][column])
                plant_obj = object_finder(-1, plant_list, row, column)
                object_finder(-1, herbivore_list, row, column).health += plant_obj.reward_value
                plant_list.remove(plant_obj)
                obstacle_tile_map[row][column] = 0
            elif agent_tile_map[row][column] == 1 and obstacle_tile_map[row][column] == 4:
                herbi_obj = object_finder(-1, herbivore_list, row, column)
                herbivore_list.remove(herbi_obj)
                # print(len(herbivore_list))
                agent_tile_map[row][column] = 0
                pygame.draw.rect(display_surface, colors(rock_color), back_tile_map[row][column], 8)
            elif agent_tile_map[row][column] == 0 and obstacle_tile_map[row][column] == 3:
                pygame.draw.rect(display_surface, colors(plant_color), back_tile_map[row][column], 5)

            elif agent_tile_map[row][column] == 0 and obstacle_tile_map[row][column] == 4:
                pygame.draw.rect(display_surface, colors(rock_color), back_tile_map[row][column], 8)
            # Carnivore
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
                # print(len(carnivore_list))
                agent_tile_map[row][column] = 0
                pygame.draw.rect(display_surface, colors(rock_color), back_tile_map[row][column], 8)

    pygame.display.update()
    clock.tick(FPS)


def object_finder(idx_avoid, object_list, row, column):
    for i in object_list:
        if i.row_number == row and i.column_number == column and i.id != idx_avoid:
            return i
    return None


def observation_list_length():  # For finding out the length of the observation list and adding 0 health on death
    obs_list = [-1] * (sum(list(range(observation_space, 0, -1))) *8)
    obs_list.append(0)
    return obs_list


def Simulation(number_of_herbivores, number_of_carnivores, number_of_plants, number_of_rocks,
               health_herbivore, health_carnivore, herbivore_reward=15, plant_reward=10, rock_reward=-2,
               sim_controller='random',
               obs_space=1, speed=30):
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
    global FPS
    global clock
    FPS = speed
    clock = pygame.time.Clock()

    global title_txt
    global title_txt_rect
    global company_txt
    global company_txt_rect
    title_txt, title_txt_rect = fonts('font3', 40, "Survive RL", (100, 25), colors('light_green'))
    company_txt, company_txt_rect = fonts('font3', 40, "Mandred Tech", (1375, 680), colors('light_red'))
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
