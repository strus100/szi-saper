import pygame
from grid import Grid
from parseros import Parser
from a_star import AStar
from is_bomb_matcher import IsBombMatcher
from PIL import Image
import random
import glob
from time import sleep

pygame.init()

display_width = 600
display_height = 600

black = (0,0,0)

gameDisplay = pygame.display.set_mode((display_width, display_height))
pygame.display.set_caption('Saper')
clock = pygame.time.Clock()

how_many_fields = 10
field_size = display_height / how_many_fields

robot_size = int(field_size * 0.8)

robotImg = pygame.image.load('images/robot.png')
robotImg = pygame.transform.scale(robotImg, (robot_size, robot_size))

bombaImg = pygame.image.load('images/bomba.png')
bombaImg = pygame.transform.scale(bombaImg, (robot_size, robot_size))

parser = Parser()
field_params = parser.parse_data("data/data.txt")

map_obj = Grid(how_many_fields, field_size, field_params)
map = map_obj.grid

def text_objects(text, font):
    textSurface = font.render(text, True, black)
    return textSurface, textSurface.get_rect()

def print_alert(text):
    print(text)
    large_text = pygame.font.Font('freesansbold.ttf', 20)
    TextSurf, TextRect = text_objects(text, large_text)
    TextRect.center = ((display_width/2), display_height/2)
    gameDisplay.blit(TextSurf, TextRect)

    pygame.display.update()


def read_photo(field, model_file, label_file):
    is_b = IsBombMatcher()
    results = is_b.get_result(field.photo, model_file, label_file)
    return results


def move_robot(field):
    gameDisplay.blit(robotImg, (field.map_x, field.map_y))


[first_field, last_field] = map_obj.first_and_last()


def scan_for_bombs():
    fields_with_bombs = []
    for y in map:
        for x in y:
            if is_bomb_here(x):
                print(x.get_position())
                fields_with_bombs.insert(len(fields_with_bombs), x)
    return fields_with_bombs


def is_bomb_here(field):
    model_file1 = "tf/tf_files_igor/retrained_graph.pb"
    label_file1 = "tf/tf_files_igor/retrained_labels.txt"
    results = read_photo(field, model_file1, label_file1)
    first_result = results[1]

    if (first_result.result_name == "bomb" and first_result.result_percent*100 > 75):
        return True
    else:
        return False


fields_with_bombs = scan_for_bombs()


def get_images(dir):
    images_list = []
    for filename in glob.glob(dir):  # assuming gif
        im = Image.open(filename)
        images_list.append(im.filename)
    return images_list

def game_loop(start_point, fields_with_bombs, flowers, last_field):
    model_file = "tf/tf_files_kuba/retrained_graph.pb"
    label_file = "tf/tf_files_kuba/retrained_labels.txt"

    a = AStar()
    current_field = start_point
    field_to_move = fields_with_bombs[0]
    fields_with_bombs.remove(field_to_move)
    path = a.find_path(current_field, field_to_move, map_obj)
    robot_x = (0)
    robot_y = (0)
    is_last_field = last_field == current_field

    gameExit = False

    while not gameExit:

        for event in pygame.event.get(): 
            if event.type == pygame.QUIT:
                pygame.quit()
                quit()

        for y in map:
            for x in y:
                gameDisplay.fill(x.color, (x.map_x, x.map_y, field_size, field_size))
                if x.has_bomb == True:
                    gameDisplay.blit(bombaImg, (x.map_x, x.map_y))

        if len(path) > 0:
            current_field = path[0]
            move_robot(current_field)
            path.remove(current_field)

        elif len(fields_with_bombs) > 0:
            field_to_move = fields_with_bombs[0]
            fields_with_bombs.remove(field_to_move)
            path = a.find_path(current_field, field_to_move, map_obj)
            move_robot(current_field)

        if current_field == field_to_move:
            make_action_with_bomb(current_field, label_file, model_file)
            remove_bomb(current_field, flowers)
            sleep(1)
            if len(fields_with_bombs) == 0:
                pygame.quit()
                quit()

        pygame.display.update()
        clock.tick(3)


def make_action_with_bomb(current_field, label_file, model_file):
    what_bomb = read_photo(current_field, model_file, label_file)[1]

    found = "Znaleziono: " + what_bomb.result_name + " na " + str(what_bomb.result_percent * 100)[:5] + "%"
    if what_bomb.result_name == "bomba":
        action = "Detonuje!, "
    elif what_bomb.result_name == "c4":
        action = "Rozbrajam!, "
    elif what_bomb.result_name == "dynamit":
        action = "Zabieram!, "
    elif what_bomb.result_name == "mina":
        action = "Detonuje!, "
    else:
        action = "To nie bomba! "

    print_alert(action + found)


def remove_bomb(current_field, flowers):
    current_field.has_bomb = False
    current_field.image = flowers[random.randrange(len(flowers))]


flowers_list = get_images('flowers/*.*')

game_loop(first_field, fields_with_bombs, flowers_list, fields_with_bombs[len(fields_with_bombs) -1])
pygame.quit()
quit()
