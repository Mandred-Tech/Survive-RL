""" 1 for Herbivore 2 for Carnivore 3 for Plants 4 for Rocks"""
""" 1 for up direction -1 for down direction -2 for left and 2 for right"""
import pygame
from config import colors, fonts


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

    def hud(self):
        pass


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


if __name__ == '__main__':
    pygame.init()
    WINDOW_WIDTH = 1500
    WINDOW_HEIGHT = 700
    display_surface = pygame.display.set_mode((WINDOW_WIDTH, WINDOW_HEIGHT))
    display_surface.fill(colors('grey'))
    pygame.display.set_caption("SURVIVE RL")

    FPS = 60
    clock = pygame.time.Clock()

    title_txt, title_txt_rect = fonts('font3', 40, "Survive RL", (100, 25), colors('light_green'))
    # pygame.draw.line(display_surface, colors('white'), (0, 45), (2000, 45), 2)
    # pygame.draw.line(display_surface, colors('white'), (0, 655), (2000, 655), 2)
    company_txt, company_txt_rect = fonts('font3', 40, "Mandred Tech", (1375, 680), colors('light_red'))
    # pygame.draw.rect(display_surface,colors('light_blue'),(0,50,1500,600),5)

    env = Environment(10, 20, 25, 1500, 600)
    back_tile_map, tile_map = env.background_tile_map_layer(50, 650, 0, 1500)
    herbivore_1 = Herbivore('red', 100, 50, 20, 10, 20)

    running = True
    while running:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                running = False
            if event.type == pygame.KEYDOWN:
                if event.key == pygame.K_UP:
                    herbivore_1.move(1)
                if event.key == pygame.K_DOWN:
                    herbivore_1.move(-1)
                if event.key == pygame.K_LEFT:
                    herbivore_1.move(-2)
                if event.key == pygame.K_RIGHT:
                    herbivore_1.move(2)

        display_surface.blit(title_txt, title_txt_rect)
        display_surface.blit(company_txt, company_txt_rect)

        pygame.display.update()
        clock.tick(FPS)

    pygame.quit()
