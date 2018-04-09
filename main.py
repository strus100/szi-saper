import pygame
from pygame.locals import *
from implementation import *
import sys
import heapq
from pip._vendor.distlib.compat import raw_input

pygame.init()


white = (255, 255, 255, 255)
OKNOGRY = pygame.display.set_mode((816, 624), 0, 32)
pygame.display.set_caption('SAPER')
x = (48)
y = (96)
mapImg = pygame.image.load('mapaSaper.png')
robotImg = pygame.image.load('robot.png')

def robot(x, y):
	OKNOGRY.blit(robotImg, (x, y))

def heuristic(a, b):

    (x1, y1) = a
    (x2, y2) = b
    OKNOGRY.blit(robotImg, (x2*48, y2*48))
    pygame.display.update()
    return abs(x1 - x2) + abs(y1 - y2)


class PriorityQueue:
    def __init__(self):
        self.elements = []

    def empty(self):
        return len(self.elements) == 0

    def put(self, item, priority):
        heapq.heappush(self.elements, (priority, item))

    def get(self):
        return heapq.heappop(self.elements)[1]


def a_star_search(graph, start, goal):
    frontier = PriorityQueue()
    frontier.put(start, 0)
    came_from = {}
    cost_so_far = {}
    came_from[start] = None
    cost_so_far[start] = 0

    while not frontier.empty():
        current = frontier.get()

        if current == goal:
            break

        for next in graph.neighbors(current):
            new_cost = cost_so_far[current] + graph.cost(current, next)
            if next not in cost_so_far or new_cost < cost_so_far[next]:
                cost_so_far[next] = new_cost
                priority = new_cost + heuristic(goal, next)
                frontier.put(next, priority)
                came_from[next] = current

    return came_from, cost_so_far


start, goal = (1, 2), (7, 8)
# came_from, cost_so_far = a_star_search(diagram4, start, goal)
# draw_grid(diagram4, width=3, point_to=came_from, start=start, goal=goal)
# print()
# draw_grid(diagram4, width=3, number=cost_so_far, start=start, goal=goal)
# print()


def krata():
    for i in range(0,13):
        for j in range(0,17):

            pygame.draw.rect(OKNOGRY, (0,0,0), Rect((j*48,i*48),(48,48)), 1)


while True:


    for event in pygame.event.get():


        if event.type == pygame.QUIT:
            pygame.quit()
            sys.exit()


    OKNOGRY.blit(mapImg, (0, 0))
    robot(x, y)
    pygame.display.update()

    # events = pygame.event.get()
    # for event in events:
    #     if event.type == pygame.KEYDOWN:
    #         if event.key == pygame.K_LEFT:
    #             robot(x+48,y)
    #         if event.key == pygame.K_RIGHT:
    #             robot(x,y + 48)



