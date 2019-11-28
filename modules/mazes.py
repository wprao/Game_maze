import pygame
import random
from modules.misc import *


class Block(object):
    def __init__(self, coordinate, block_size, border_size, **kwargs):
        # (col, row)
        self.coordinate = coordinate
        self.block_size = block_size
        self.border_size = border_size
        self.is_visited = False
        # 上下左右有没有墙
        self.has_walls = [True, True, True, True]
        self.color = (0, 0, 0)

    '''画到屏幕上'''

    def draw(self, screen):
        directions = ['top', 'bottom', 'left', 'right']
        for idx, direction in enumerate(directions):
            if self.has_walls[idx]:
                if direction == 'top':
                    x1 = self.coordinate[0] * self.block_size + self.border_size[0]
                    y1 = self.coordinate[1] * self.block_size + self.border_size[1]
                    x2 = (self.coordinate[0] + 1) * self.block_size + self.border_size[0]
                    y2 = self.coordinate[1] * self.block_size + self.border_size[1]
                    pygame.draw.line(screen, self.color, (x1, y1), (x2, y2))
                elif direction == 'bottom':
                    x1 = self.coordinate[0] * self.block_size + self.border_size[0]
                    y1 = (self.coordinate[1] + 1) * self.block_size + self.border_size[1]
                    x2 = (self.coordinate[0] + 1) * self.block_size + self.border_size[0]
                    y2 = (self.coordinate[1] + 1) * self.block_size + self.border_size[1]
                    pygame.draw.line(screen, self.color, (x1, y1), (x2, y2))
                elif direction == 'left':
                    x1 = self.coordinate[0] * self.block_size + self.border_size[0]
                    y1 = self.coordinate[1] * self.block_size + self.border_size[1]
                    x2 = self.coordinate[0] * self.block_size + self.border_size[0]
                    y2 = (self.coordinate[1] + 1) * self.block_size + self.border_size[1]
                    pygame.draw.line(screen, self.color, (x1, y1), (x2, y2))
                elif direction == 'right':
                    x1 = (self.coordinate[0] + 1) * self.block_size + self.border_size[0]
                    y1 = self.coordinate[1] * self.block_size + self.border_size[1]
                    x2 = (self.coordinate[0] + 1) * self.block_size + self.border_size[0]
                    y2 = (self.coordinate[1] + 1) * self.block_size + self.border_size[1]
                    pygame.draw.line(screen, self.color, (x1, y1), (x2, y2))
        return True


class RandomMaze(object):
    def __init__(self, maze_size, block_size, border_size, arithmetic, **kwargs):
        self.block_size = block_size
        self.border_size = border_size
        self.maze_size = maze_size
        if arithmetic == 'Prim':
            self.blocks_list = RandomMaze.createMaze_Prim(maze_size, block_size, border_size)
        else:
            pass
            # self.blocks_list=RandomMaze.createMaze_DFS(maze_size,block_size,)
        self.font = pygame.font.SysFont('Consolas', 15)

    '''画到屏幕上'''

    def draw(self, screen):
        for row in range(self.maze_size[0]):
            for col in range(self.maze_size[1]):
                self.blocks_list[row][col].draw(screen)
        # 起点和终点标志
        Label(screen, self.font, 'S', (255, 0, 0), (self.border_size[0] - 10, self.border_size[1]))
        Label(screen, self.font, 'D', (255, 0, 0), (self.border_size[0] + (self.maze_size[1] - 1) * self.block_size,
                                                    self.border_size[1] + self.maze_size[0] * self.block_size + 5))

    '''创建迷宫'''

    @staticmethod
    def createMaze_Prim(maze_size, block_size, border_size):
        blocks_list = [[Block([col, row], block_size, border_size) for col in range(maze_size[1])] for row in
                       range(maze_size[0])]
        block_now = blocks_list[0][0]
        records = [block_now]
        while records:
            block_now = random.choice(records)
            block_now.is_visited = True
            records.remove(block_now)
            check = []
            x,y=block_now.coordinate[0],block_now.coordinate[1]
            if y > 0:
                if blocks_list[block_now.coordinate[0]][block_now.coordinate[1]-1].is_visited==True:
                    check.append('L')

        return blocks_list
