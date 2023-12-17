""" 1 for Herbivore 2 for Carnivore 3 for Plants 4 for Rocks"""
""" 1 for up direction -1 for down direction -2 for left and 2 for right"""
import pygame
from config import colors, fonts
import random


class Environment:
    def __init__(self, number_of_plants, number_of_rocks, size_of_tile, window_width, window_height):
        self.number_of_plants = number_of_plants
        self.number_of_rocks = number_of_rocks
        self.size_of_tile = size_of_tile
        self.window_width = window_width
        self.window_height = window_height
        self.number_of_rows = self.window_height // self.size_of_tile
        self.number_of_columns = self.window_width // self.size_of_tile

    def background_tile_map_layer(self, start_row, end_row, start_column, end_column):
        background_tile_map = [[0] * self.number_of_columns for i in range(0, self.number_of_rows)]
        tile_map = [[0] * self.number_of_columns for i in range(0, self.number_of_rows)]
        print(len(background_tile_map), len(background_tile_map[0]))
        for row in range(0, len(background_tile_map)):
            for column in range(0, len(background_tile_map[0])):
                rect = pygame.draw.rect(display_surface, colors('light_blue'),
                                        (column * self.size_of_tile, (row * self.size_of_tile) + 50,
                                        self.size_of_tile - 1, self.size_of_tile - 1), 2)
                background_tile_map[row][column] = pygame.Rect(rect)
        return background_tile_map, tile_map

    def environment_setter(self, number_of_herbivores, time_herbivore, memory_herbivore, storage_herbivore,
                        number_of_carnivores, time_carnivore, memory_carnivore, storage_carnivore):
        total_randoms = number_of_carnivores + number_of_herbivores + self.number_of_plants + self.number_of_rocks
        random_rows = [random.randint(0, self.number_of_rows - 1) for _ in range(0, total_randoms)]
        random_columns = random.sample(range(0, self.number_of_columns), total_randoms)
        herbivore_list = []
        carnivore_list = []
        plant_list = []
        rock_list = []
        for i in range(0, number_of_herbivores+ number_of_carnivores):
            if (i< number_of_herbivores):
                herbivore_list.append(Herbivore("red", time_herbivore, memory_herbivore, storage_herbivore, random_rows[i],
                                            random_columns[i]))
            else:
                carnivore_list.append(Carnivore("green", time_carnivore, memory_carnivore, storage_carnivore,
                                            random_rows[i],
                                            random_columns[i]))
        return herbivore_list, carnivore_list

class Herbivore:
    def __init__(self, color, time_limit, memory_capacity, storage_capacity, row_number, column_number):
        self.color = color
        self.time_limit = time_limit
        self.memory_capacity = memory_capacity
        self.storage_capacity = storage_capacity
        self.row_number = row_number
        self.column_number = column_number
        self.memory = [0] * self.memory_capacity
        self.storage = [0] * self.storage_capacity
        pygame.draw.rect(display_surface, colors('red'), back_tile_map[row_number][column_number])
        tile_map[row_number][column_number] = 1

    def move(self, direction):
        match direction:
            case 1:
                pygame.draw.rect(display_surface, colors('grey'), back_tile_map[self.row_number][self.column_number])
                tile_map[self.row_number][self.column_number] = 0
                pygame.draw.rect(display_surface, colors('light_blue'), back_tile_map[self.row_number][self.column_number], 2)
                self.row_number -= 1
                self.row_checker()
                tile_map[self.row_number][self.column_number] = 1
                pygame.draw.rect(display_surface, colors(self.color), back_tile_map[self.row_number][self.column_number])
            case -1:
                pygame.draw.rect(display_surface, colors('grey'), back_tile_map[self.row_number][self.column_number])
                tile_map[self.row_number][self.column_number] = 0
                pygame.draw.rect(display_surface, colors('light_blue'), back_tile_map[self.row_number][self.column_number], 2)
                self.row_number += 1
                self.row_checker()
                tile_map[self.row_number][self.column_number] = 1
                pygame.draw.rect(display_surface, colors(self.color),back_tile_map[self.row_number][self.column_number])
            case 2:
                pygame.draw.rect(display_surface, colors('grey'), back_tile_map[self.row_number][self.column_number])
                tile_map[self.row_number][self.column_number] = 0
                pygame.draw.rect(display_surface, colors('light_blue'),
                                back_tile_map[self.row_number][self.column_number], 2)
                self.column_number += 1
                self.column_checker()
                tile_map[self.row_number][self.column_number] = 1
                pygame.draw.rect(display_surface, colors(self.color),
                                back_tile_map[self.row_number][self.column_number])
            case -2:
                pygame.draw.rect(display_surface, colors('grey'), back_tile_map[self.row_number][self.column_number])
                tile_map[self.row_number][self.column_number] = 0
                pygame.draw.rect(display_surface, colors('light_blue'),
                                 back_tile_map[self.row_number][self.column_number], 2)
                self.column_number -= 1
                self.column_checker()
                tile_map[self.row_number][self.column_number] = 1
                pygame.draw.rect(display_surface, colors(self.color),
                                 back_tile_map[self.row_number][self.column_number])

    def row_checker(self):
        if self.row_number < 0:
            self.row_number = len(tile_map) - 1
        if self.row_number > len(tile_map) - 1:
            self.row_number = 0

    def column_checker(self):
        if self.column_number < 0:
            self.column_number = len(tile_map[0]) - 1
        if self.column_number > len(tile_map[0]) - 1:
            self.column_number = 0
    
    def update_memory(self, new_value):
        self.memory.insert(0, new_value)
        if len(self.memory) > self.memory_capacity:
            self.memory = self.memory[:self.memory_capacity]

class Carnivore:
    def __init__(self, color, time_limit, memory_capacity, storage_capacity, row_number, column_number):
        self.color = color
        self.time_limit = time_limit
        self.memory_capacity = memory_capacity
        self.storage_capacity = storage_capacity
        self.row_number = row_number
        self.column_number = column_number
        self.memory = [0] * self.memory_capacity
        self.storage = [0] * self.storage_capacity
        pygame.draw.rect(display_surface, colors('green'), back_tile_map[row_number][column_number])
        tile_map[row_number][column_number] = 2


    def move(self, direction):
        match direction:
            case 1:
                pygame.draw.rect(display_surface, colors('grey'), back_tile_map[self.row_number][self.column_number])
                tile_map[self.row_number][self.column_number] = 0
                pygame.draw.rect(display_surface, colors('light_blue'),
                                 back_tile_map[self.row_number][self.column_number], 2)
                self.row_number -= 1
                self.row_checker()
                tile_map[self.row_number][self.column_number] = 1
                pygame.draw.rect(display_surface, colors(self.color),
                                 back_tile_map[self.row_number][self.column_number])
            case -1:
                pygame.draw.rect(display_surface, colors('grey'), back_tile_map[self.row_number][self.column_number])
                tile_map[self.row_number][self.column_number] = 0
                pygame.draw.rect(display_surface, colors('light_blue'),
                                 back_tile_map[self.row_number][self.column_number], 2)
                self.row_number += 1
                self.row_checker()
                tile_map[self.row_number][self.column_number] = 1
                pygame.draw.rect(display_surface, colors(self.color),
                                 back_tile_map[self.row_number][self.column_number])
            case 2:
                pygame.draw.rect(display_surface, colors('grey'), back_tile_map[self.row_number][self.column_number])
                tile_map[self.row_number][self.column_number] = 0
                pygame.draw.rect(display_surface, colors('light_blue'),
                                 back_tile_map[self.row_number][self.column_number], 2)
                self.column_number += 1
                self.column_checker()
                tile_map[self.row_number][self.column_number] = 1
                pygame.draw.rect(display_surface, colors(self.color),
                                back_tile_map[self.row_number][self.column_number])
            case -2:
                pygame.draw.rect(display_surface, colors('grey'), back_tile_map[self.row_number][self.column_number])
                tile_map[self.row_number][self.column_number] = 0
                pygame.draw.rect(display_surface, colors('light_blue'),
                                back_tile_map[self.row_number][self.column_number], 2)
                self.column_number -= 1
                self.column_checker()
                tile_map[self.row_number][self.column_number] = 1
                pygame.draw.rect(display_surface, colors(self.color),
                                back_tile_map[self.row_number][self.column_number])

    def row_checker(self):
        if self.row_number < 0:
            self.row_number = len(tile_map) - 1
        if self.row_number > len(tile_map) - 1:
            self.row_number = 0

    def column_checker(self):
        if self.column_number < 0:
            self.column_number = len(tile_map[0]) - 1
        if self.column_number > len(tile_map[0]) - 1:
            self.column_number = 0
    
    def update_memory(self, new_value):
        self.memory.insert(0, new_value)
        if len(self.memory) > self.memory_capacity:
            self.memory = self.memory[:self.memory_capacity]

    def eat_herbivore(self, herbivore):
        if self.row_number == herbivore.row_number and self.column_number == herbivore.column_number:
            # Carnivore gains memory and time_limit from herbivore
            self.memory += herbivore.memory
            self.time_limit += herbivore.time_limit

            # Remove herbivore from the tile_map
            tile_map[herbivore.row_number][herbivore.column_number] = 0

            # Optionally, reset herbivore's memory and time_limit
            herbivore.memory = [0] * herbivore.memory_capacity
            herbivore.time_limit = 0

            # Optionally, move carnivore to the herbivore's position
            pygame.draw.rect(display_surface, colors('grey'), back_tile_map[self.row_number][self.column_number])
            tile_map[self.row_number][self.column_number] = 0

            self.row_number = herbivore.row_number
            self.column_number = herbivore.column_number

            pygame.draw.rect(display_surface, colors('blue'), back_tile_map[self.row_number][self.column_number])
            tile_map[self.row_number][self.column_number] = 2



if __name__ == '__main__':
    number_herbivores = int(input("Enter the number of Herbivores"))
    number_carnivores = int(input("Enter the number of Carnivores"))
    pygame.init()
    WINDOW_WIDTH = 1250
    WINDOW_HEIGHT = 630
    display_surface = pygame.display.set_mode((WINDOW_WIDTH, WINDOW_HEIGHT))
    display_surface.fill(colors('grey'))
    pygame.display.set_caption("SURVIVE RL")

    FPS = 60
    clock = pygame.time.Clock()

    title_txt, title_txt_rect = fonts('font3', 40, "Survive RL", (100, 25), colors('light_green'))
    company_txt, company_txt_rect = fonts('font3', 40, "Mandred Tech", (1375, 680), colors('light_red'))

    env = Environment(10, 5, 25, 1500, 600)
    back_tile_map, tile_map = env.background_tile_map_layer(50, 650, 0, 1500)

    herbivore_list, carnivore_list = env.environment_setter(number_herbivores, 1, 1, 1, number_carnivores, 1, 1, 1)

    # Draw entities before entering the main loop
    # Draw herbivores
    for herbivore in herbivore_list:
        pygame.draw.rect(display_surface, colors('red'), back_tile_map[herbivore.row_number][herbivore.column_number])

    # Draw carnivores
    for carnivore in carnivore_list:
        pygame.draw.rect(display_surface, colors('blue'), back_tile_map[carnivore.row_number][carnivore.column_number])

    user_chooses_herbivore = True  # Start with herbivore selected
    selected_entity = herbivore_list[0]  # Default to the first herbivore

    running = True
    while running:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                running = False
            if event.type == pygame.KEYDOWN:
                entity_to_move = selected_entity
                if event.key == pygame.K_UP:
                    entity_to_move.move(1)
                if event.key == pygame.K_DOWN:
                    entity_to_move.move(-1)
                if event.key == pygame.K_LEFT:
                    entity_to_move.move(-2)
                if event.key == pygame.K_RIGHT:
                    entity_to_move.move(2)
                if event.key == pygame.K_h:  # Press 'h' to choose herbivore
                    user_chooses_herbivore = True
                    selected_entity = herbivore_list[0]  # Default to the first herbivore
                if event.key == pygame.K_c:  # Press 'c' to choose carnivore
                    user_chooses_herbivore = False
                    selected_entity = carnivore_list[0]  # Default to the first carnivore

        # Update entities
        for herbivore in herbivore_list:
            herbivore.update_memory(42)

        for carnivore in carnivore_list:
            carnivore.update_memory(42)

        # Draw background
        for row in range(len(back_tile_map)):
            for column in range(len(back_tile_map[0])):
                pygame.draw.rect(display_surface, colors('light_blue'), back_tile_map[row][column], 2)

        # Draw herbivores
        for herbivore in herbivore_list:
            pygame.draw.rect(display_surface, colors('red'), back_tile_map[herbivore.row_number][herbivore.column_number])

        # Draw carnivores
        for carnivore in carnivore_list:
            pygame.draw.rect(display_surface, colors('blue'), back_tile_map[carnivore.row_number][carnivore.column_number])

        display_surface.blit(title_txt, title_txt_rect)
        display_surface.blit(company_txt, company_txt_rect)

        pygame.display.update()
        clock.tick(FPS)

    pygame.quit()
