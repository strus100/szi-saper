import pygame

from grid import Grid
from txt_parser import TxtParser
from a_star import AStar

pygame.init()

display_width = 1000
display_height = 1000

black = (0,0,0)
white = (255,255,255)

gameDisplay = pygame.display.set_mode((display_width, display_height))

pygame.display.set_caption('Saper')

clock = pygame.time.Clock()

robot_width = 80
robot_height = 80

robotImg = pygame.image.load('../images/robot.png')
robotImg = pygame.transform.scale(robotImg, (robot_width, robot_height))

bombaImg = pygame.image.load('../images/bomba.png')
bombaImg = pygame.transform.scale(bombaImg, (robot_width, robot_height))

field_width = 100
field_height = 100

parser = TxtParser()
field_params = parser.parse("../data/data.txt")

map_obj = Grid(10,10, field_width, field_height, field_params)
map = map_obj.grid

def text_objects(text, font):
    textSurface = font.render(text, True, black)
    return textSurface, textSurface.get_rect()

def print_alert():
    text = "O mamuniu, bomba"
    
    large_text = pygame.font.Font('freesansbold.ttf', 90)
    TextSurf, TextRect = text_objects(text, large_text)
    TextRect.center = ((display_width/2), display_height/2)
    gameDisplay.blit(TextSurf, TextRect)

    pygame.display.update()


def move_robot(field):
    if field.has_bomb == True:
        print_alert()
    gameDisplay.blit(robotImg, (field.x, field.y))


[first_field, last_field] = map_obj.first_and_last()

def scan_for_bombs():
    fields_with_bombs = []
    for y in map:
        for x in y:
            if x.has_bomb:
                fields_with_bombs.insert(len(fields_with_bombs), x)
    return fields_with_bombs

fields_with_bombs = scan_for_bombs()
# path_to_first_bomb = find_path(first_field, first_bomb)


def game_loop(start_point, fields_with_bombs):
    a = AStar()
    current_field = start_point
    field_to_move = fields_with_bombs[0]
    fields_with_bombs.remove(field_to_move)
    path = a.find_path(current_field, field_to_move, map_obj)
    robot_x = (0)
    robot_y = (0)

    gameExit = False

    while not gameExit: 
        for event in pygame.event.get(): 
            if event.type == pygame.QUIT:
                pygame.quit()
                quit()

        gameDisplay.fill(white)
        for y in map:
            for x in y:
                gameDisplay.fill(x.color, (x.x, x.y, field_width, field_height))
                if x.has_bomb == True:
                    gameDisplay.blit(bombaImg, (x.x, x.y))

        if len(path) > 0:
            current_field = path[0]
            move_robot(current_field)
            path.remove(current_field)

        elif len(fields_with_bombs) > 0:
            field_to_move = fields_with_bombs[0]
            fields_with_bombs.remove(field_to_move)
            path = a.find_path(current_field, field_to_move, map_obj)
            move_robot(current_field)
        
        pygame.display.update()
        clock.tick(3)


game_loop(first_field, fields_with_bombs)
pygame.quit()
quit()
