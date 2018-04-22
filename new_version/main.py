import pygame
import time
import random

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


[first_field, last_field] = map_obj.first_and_last()
print(first_field.get_position())
find_path(first_field, last_field)

# def text_objects(text, font):
#     textSurface = font.render(text, True, black)
#     return textSurface, textSurface.get_rect()

# def message_display(text):
#     large_text = pygame.font.Font('freesansbold.ttf', 115)
#     TextSurf, TextRect = text_objects(text, large_text)
#     TextRect.center = ((display_width/2), display_height/2)
#     gameDisplay.blit(TextSurf, TextRect)

#     pygame.display.update()

#     time.sleep(2)

#     game_loop()

def game_loop():

    robot_x = (display_width * 0.4)
    robot_y = (display_height - robot_height)

    gameExit = False

    while not gameExit: 
        for event in pygame.event.get(): 
            if event.type == pygame.QUIT:
                pygame.quit()
                quit()
        #     if event.type == pygame.KEYDOWN:
        #         if event.key == pygame.K_LEFT:
        #             x_change = -5
        #         elif event.key == pygame.K_RIGHT:
        #             x_change = 5

        #     if event.type == pygame.KEYUP:
        #         if event.key == pygame.K_LEFT or event.key == pygame.K_RIGHT:
        #             x_change = 0

        # x += x_change

        gameDisplay.fill(white)
        if random.randrange(2) == 1:
            for y in map:
                for x in y:
                    gameDisplay.fill(x.color, (x.x, x.y, field_width, field_height))
                    if x.has_bomb == True:
                        gameDisplay.blit(bombaImg, (x.x, x.y))

            if len(map_obj.path) > 0:
                for field in map_obj.path:
                    gameDisplay.fill((0,0,255), (field.x, field.y, field_width, field_height))
        else:
            if len(map_obj.path) > 0:
                for field in map_obj.path:
                    gameDisplay.fill((0,0,255), (field.x, field.y, field_width, field_height))

            for y in map:
                for x in y:
                    gameDisplay.fill(x.color, (x.x, x.y, field_width, field_height))
                    if x.has_bomb == True:
                        gameDisplay.blit(bombaImg, (x.x, x.y))


        robot(robot_x, robot_y)

        pygame.display.update()
        clock.tick(5)

game_loop()
pygame.quit()
quit()