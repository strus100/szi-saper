import pygame
import time
import random
import time

from field import Field
from grid import Grid

pygame.init()

display_width = 1000
display_height = 1000

black = (0,0,0)
white = (255,255,255)

gameDisplay = pygame.display.set_mode((display_width, display_height))

pygame.display.set_caption('Saper')

clock = pygame.time.Clock()

# size of robot img
robot_width = 80
robot_height = 80

robotImg = pygame.image.load('robot.png')
robotImg = pygame.transform.scale(robotImg, (robot_width, robot_height))

bombaImg = pygame.image.load('bomba.png')
bombaImg = pygame.transform.scale(bombaImg, (robot_width, robot_height))


field_width = 100
field_height = 100

map_obj = Grid(10,10, field_width, field_height)
map = map_obj.grid

# find_path takes `Field` objects 
def find_path(start_field, target_field):
    open_set = []
    closed_set = []
    open_set.insert(0, start_field)

    while len(open_set) > 0:
        current_field = open_set[0]
        for open_field in open_set:
            if open_field.f_cost() < current_field.f_cost() or open_field.f_cost == current_field.f_cost and open_field.h_cost < current_field.h_cost:
                current_field = open_field

        open_set.remove(current_field)
        closed_set.insert(len(closed_set), current_field)

        if current_field == target_field:
            print("ZNALAZLEM")
            retrace_path(start_field, target_field)
            return
        
        # print(map_obj.get_neighbours(current_field))

        for neighbour in map_obj.get_neighbours(current_field):
            if not neighbour.walkable or neighbour in closed_set:
                continue

            new_movement_cost_to_neighbour = current_field.g_cost + get_distance(current_field, neighbour)
            if new_movement_cost_to_neighbour < neighbour.g_cost or not neighbour in open_set:
                neighbour.g_cost = new_movement_cost_to_neighbour
                neighbour.h_cost = get_distance(neighbour, target_field)
                neighbour.set_parent(current_field)

                if not neighbour in open_set:
                    open_set.insert(len(open_set), neighbour)
        
def retrace_path(start_field, end_node):
    path = []
    current_field = end_node
    
    while (current_field != start_field):
        path.insert(len(path), current_field)
        current_field = current_field.parent

    path.insert(len(path), start_field)
    path = path[::-1]
    map_obj.set_path(path)

    for field in path:
        print(field.get_position())


def get_distance(field_a, field_b):
    dist_x = abs(field_a.x - field_b.x)
    dist_y = abs(field_a.y - field_b.y)

    if dist_x > dist_y:
        return 14*dist_y + 10*(dist_x-dist_y)
    return 14*dist_y + 10*(dist_y-dist_x)

def robot(x,y):
    gameDisplay.blit(robotImg, (x, y))

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


def move_robot(path):
    field = path[0]
    if field.has_bomb == True:
        print_alert()
    gameDisplay.blit(robotImg, (field.x, field.y))
    path.remove(field)
    return path


[first_field, last_field] = map_obj.first_and_last()
print(first_field.get_position())
find_path(first_field, last_field)

def game_loop():

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

        if len(map_obj.path) > 0:
            map_obj.set_path(move_robot(map_obj.path))
        else:
            robot(0,0)
           
        pygame.display.update()
        clock.tick(1)

game_loop()
pygame.quit()
quit()
