# class coordinate(object):
#     def __init__(self, x, y):
#         self.x = x;
#         self.y = y;


list = [[(x, y) for y in range(0, 5)] for x in range(0, 10)]
print(list)

a = (1, 2)
b = (3, 4)
print(a + b)

import pygame
import sys
import random


def isvisited(screen, position, color=(255, 0, 0)):
    pygame.draw.circle(screen, color, position,2)


pygame.init()
pygame.font.init()
screen = pygame.display.set_mode((800, 680))
screen.fill((255, 255, 255))
isvisited(screen,(500,300))
pygame.display.update()
while True:
    for event in pygame.event.get():
        if event.type==pygame.QUIT:
            pygame.quit()
            sys.exit(-1)
pygame.display.update()
