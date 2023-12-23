""" 1 for Herbivore 2 for Carnivore 3 for Plants 4 for Rocks"""
""" 1 for up direction 2 for down direction 3 for left and 4 for right"""
import pygame
from config import colors, fonts
import random
from itertools import product


class Environment:
    def __init__(self, number_of_herbivores, number_of_carnivores, number_of_plants, number_of_rocks,
                 health_herbivore=100, health_carnivore=100):
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
        print(self.number_of_rows,self.number_of_columns)

    def background_tile_map_layer(self, start_row, end_row, start_column, end_column):
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
        sample_combinations=list(product(list(range(0,self.number_of_rows)),list(range(0,self.number_of_columns))))
        required_sample=random.sample(sample_combinations,total_randoms)
        herbivore_list = []
        carnivore_list = []
        plant_list = []
        rock_list = []
        for i in range(0,self.number_of_herbivores):
            herbivore_list.append(Herbivore(i,herbivore_color,100,required_sample[i][0],required_sample[i][1]))
        for i in range(self.number_of_herbivores,self.number_of_herbivores+self.number_of_plants):
            plant_list.append(Plant(i,plant_color,10,required_sample[i][0],required_sample[i][1]))


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
        match direction:
            case 1:
                self.row_number -= 1
                self.row_number = row_checker(self.row_number)
            case 2:
                self.row_number += 1
                self.row_number = row_checker(self.row_number)
            case 4:
                self.column_number += 1
                self.column_number = column_checker(self.column_number)
            case 3:
                self.column_number -= 1
                self.column_number = column_checker(self.column_number)

        if agent_tile_map[self.row_number][self.column_number] == 1:
            agent_tile_map[prev_row][prev_col] = 1
        else:
            agent_tile_map[prev_row][prev_col] = 0
            agent_tile_map[self.row_number][self.column_number] = 1
        updater()
        # print(agent_tile_map[self.row_number][self.column_number],agent_tile_map[prev_row][prev_col])
        # print(obstacle_tile_map[self.row_number][self.column_number],obstacle_tile_map[prev_row][prev_col])


class Plant:
    def __init__(self, identifier, color, value, row_number, column_number):
        self.id = identifier
        self.color = color
        self.reward_value = value
        self.row_number = row_number
        self.column_number = column_number
        self.storage = [0]
        pygame.draw.rect(display_surface, colors(self.color), back_tile_map[row_number][column_number], 5)
        obstacle_tile_map[row_number][column_number] = 3


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


def updater():
    for row in range(0, len(back_tile_map)):
        for column in range(0, len(back_tile_map[0])):
            pygame.draw.rect(display_surface, colors('grey'), back_tile_map[row][column])
            pygame.draw.rect(display_surface, colors('light_blue'),
                             back_tile_map[row][column], 2)
            if agent_tile_map[row][column] == 1 and obstacle_tile_map[row][column] == 0:
                pygame.draw.rect(display_surface, colors(herbivore_color), back_tile_map[row][column])
            elif agent_tile_map[row][column] == 1 and obstacle_tile_map[row][column] == 3:
                pygame.draw.rect(display_surface, colors(herbivore_color), back_tile_map[row][column])
                pygame.draw.rect(display_surface, colors(plant_color), back_tile_map[row][column], 5)
            elif agent_tile_map[row][column] == 0 and obstacle_tile_map[row][column] == 3:
                pygame.draw.rect(display_surface, colors(plant_color), back_tile_map[row][column], 5)


if __name__ == '__main__':
    pygame.init()
    WINDOW_WIDTH = 1500
    WINDOW_HEIGHT = 700
    display_surface = pygame.display.set_mode((WINDOW_WIDTH, WINDOW_HEIGHT))
    display_surface.fill(colors('grey'))
    pygame.display.set_caption("SURVIVE RL")
    herbivore_color = 'red'
    plant_color = 'green'

    FPS = 60
    clock = pygame.time.Clock()

    title_txt, title_txt_rect = fonts('font3', 40, "Survive RL", (100, 25), colors('light_green'))
    company_txt, company_txt_rect = fonts('font3', 40, "Mandred Tech", (1375, 680), colors('light_red'))

    env = Environment(5, 5, 10, 10)
    back_tile_map, agent_tile_map, obstacle_tile_map = env.background_tile_map_layer(50, 650, 0, 1500)
    herbivore_1 = Herbivore(20,'red', 100, 15, 10)
    env.environment_setter()

    running = True
    while running:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                running = False
            if event.type == pygame.KEYDOWN:
                if event.key == pygame.K_UP:
                    herbivore_1.move(1)
                if event.key == pygame.K_DOWN:
                    herbivore_1.move(2)
                if event.key == pygame.K_LEFT:
                    herbivore_1.move(3)
                if event.key == pygame.K_RIGHT:
                    herbivore_1.move(4)

        display_surface.blit(title_txt, title_txt_rect)
        display_surface.blit(company_txt, company_txt_rect)

        pygame.display.update()
        clock.tick(FPS)

    pygame.quit()
