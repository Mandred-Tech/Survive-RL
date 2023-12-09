import pygame


def colors(color):  # Function to define colors used in the environment
    white = (255, 255, 255)
    black = (0, 0, 0)
    grey = (96, 96, 96)
    red = (255, 0, 0)
    green = (0, 255, 0)
    blue = (0, 0, 255)
    light_red = (255, 102, 102)
    light_green = (102, 255, 102)
    light_blue = (102, 255, 255)
    match color:
        case 'white':
            return white
        case 'black':
            return black
        case 'red':
            return red
        case 'green':
            return green
        case 'blue':
            return blue
        case 'light_red':
            return light_red
        case 'light_green':
            return light_green
        case 'light_blue':
            return light_blue
        case 'grey':
            return grey


def fonts(font_name, size, text, location, color):  # Function to define fonts
    font1 = pygame.font.Font(r'D:\My_programing_projects\Survive_RL\Fonts\aware-font\AwareBold-qZo3x.ttf', size)
    font2 = pygame.font.Font(r'D:\My_programing_projects\Survive_RL\Fonts\fonarto-2-font\FonartoRegular-8Mon2.ttf',
                             size)
    font3 = pygame.font.Font(r'D:\My_programing_projects\Survive_RL\Fonts\stepalange-font\Stepalange-x3BLm.otf', size)

    match font_name:
        case 'font1':
            text_obj = font1.render(text, True, color)
            text_obj_rect = text_obj.get_rect()
            text_obj_rect.center = location
            return text_obj, text_obj_rect
        case 'font2':
            text_obj = font2.render(text, True, color)
            text_obj_rect = text_obj.get_rect()
            text_obj_rect.center = location
            return text_obj, text_obj_rect
        case 'font3':
            text_obj = font3.render(text, True, color)
            text_obj_rect = text_obj.get_rect()
            text_obj_rect.center = location
            return text_obj, text_obj_rect
