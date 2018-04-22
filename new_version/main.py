import pygame
import time
import random

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

robotImg = pygame.image.load('robot.png')
robotImg = pygame.transform.scale(robotImg, (robot_width, robot_height))

# horizontal = []
# map = [horizontal]
map = []
field_width = 100
field_height = 100

def rand_color():
    color = (random.randrange(255), random.randrange(255), random.randrange(255))
    print(color)
    return color

def generate_map():
    for i in range(0,10):
        horizontal = []
        for j in range(0,10):
            field = {
                'x': j,
                'y': i,
                'params': {
                    'is_bomb': False
                },
                'color': rand_color()
            }
            horizontal.insert(len(horizontal), field)
        map.insert(len(map), horizontal)



generate_map()
 

def robot(x,y):
    gameDisplay.blit(robotImg, (x, y))

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

# def crash():
#     message_display('You Crashed')


def game_loop():

    robot_x = (display_width * 0.4)
    robot_y = (display_height * 0.8)

    x_change = 0

    gameExit = False

    while not gameExit: 
        # for event in pygame.event.get(): 
        #     if event.type == pygame.QUIT:
        #         pygame.quit()
        #         quit()
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

        for index, y in enumerate(map):
            # print(index)
            for x_index, x in enumerate(map[index]):
                x_value = x_index * field_width
                y_value = index * field_height
                color = x['color']
                gameDisplay.fill(color, (x_value, y_value, field_width, field_height))
        
        robot(robot_x, robot_y)

        # if x > display_width - robot_width or x < 0:
        #     crash()

        pygame.display.update()
        clock.tick(60)

game_loop()
pygame.quit()
quit()