'''
Function:
	随机生成迷宫
'''
import pygame
import cfg
import random
from modules.misc import *

'''一个游戏地图块'''


class Block():
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


'''随机生成迷宫类'''


class RandomMaze():
    # maze_size:迷宫大小；block_size:格子大小;border_size:边框大小
    def __init__(self, maze_size, block_size, border_size, arithmetic, starting_point, destination, **kwargs):
        self.block_size = block_size
        self.border_size = border_size
        self.maze_size = maze_size
        self.starting_point = starting_point
        self.destination = destination
        # if arithmetic == 'Prim':
        #     self.blocks_list = RandomMaze.createMaze_Prim(maze_size, block_size, border_size)
        # else:
        #     self.blocks_list = RandomMaze.createMaze_DFS(maze_size, block_size, border_size)
        self.blocks_list = RandomMaze.createMaze(maze_size, block_size, border_size)
        self.font = pygame.font.SysFont(cfg.FONT, 12)

    '''画到屏幕上'''

    def draw(self, screen):
        for row in range(self.maze_size[0]):
            for col in range(self.maze_size[1]):
                self.blocks_list[row][col].draw(screen)
        # 起点和终点标志
        Label_ce(screen, self.font, 'S', (255, 0, 0),
                 (self.starting_point[1] * self.block_size + self.border_size[0]+8, self.starting_point[
                     0] * self.block_size + self.border_size[1]+8))
        # Label_co(screen, self.font, 'S', (255, 0, 0), (self.border_size[0] - 10, self.border_size[1]))
        Label_ce(screen, self.font, 'D', (255, 0, 0),
                 (self.destination[1] * self.block_size + self.border_size[0]+8, self.destination[
                     0] * self.block_size + self.border_size[1]+8))

    '''创建迷宫'''

    @staticmethod
    def createMaze(maze_size, block_size, border_size):
        def nextBlock(block_now, blocks_list):
            directions = ['top', 'bottom', 'left', 'right']
            blocks_around = dict(zip(directions, [None] * 4))
            block_next = None
            count = 0
            # 查看上边block
            if block_now.coordinate[1] - 1 >= 0:
                block_now_top = blocks_list[block_now.coordinate[1] - 1][block_now.coordinate[0]]
                if not block_now_top.is_visited:
                    blocks_around['top'] = block_now_top
                    count += 1
            # 查看下边block
            if block_now.coordinate[1] + 1 < maze_size[0]:
                block_now_bottom = blocks_list[block_now.coordinate[1] + 1][block_now.coordinate[0]]
                if not block_now_bottom.is_visited:
                    blocks_around['bottom'] = block_now_bottom
                    count += 1
            # 查看左边block
            if block_now.coordinate[0] - 1 >= 0:
                block_now_left = blocks_list[block_now.coordinate[1]][block_now.coordinate[0] - 1]
                if not block_now_left.is_visited:
                    blocks_around['left'] = block_now_left
                    count += 1
            # 查看右边block
            if block_now.coordinate[0] + 1 < maze_size[1]:
                block_now_right = blocks_list[block_now.coordinate[1]][block_now.coordinate[0] + 1]
                if not block_now_right.is_visited:
                    blocks_around['right'] = block_now_right
                    count += 1
            if count > 0:
                while True:
                    direction = random.choice(directions)
                    if blocks_around.get(direction):
                        block_next = blocks_around.get(direction)
                        if direction == 'top':
                            block_next.has_walls[1] = False
                            block_now.has_walls[0] = False
                        elif direction == 'bottom':
                            block_next.has_walls[0] = False
                            block_now.has_walls[1] = False
                        elif direction == 'left':
                            block_next.has_walls[3] = False
                            block_now.has_walls[2] = False
                        elif direction == 'right':
                            block_next.has_walls[2] = False
                            block_now.has_walls[3] = False
                        break
            return block_next

        blocks_list = [[Block([col, row], block_size, border_size) for col in range(maze_size[1])] for row in
                       range(maze_size[0])]
        block_now = blocks_list[0][0]
        records = []
        while True:
            if block_now:
                if not block_now.is_visited:
                    block_now.is_visited = True
                    records.append(block_now)
                block_now = nextBlock(block_now, blocks_list)
            else:
                block_now = records.pop()
                if len(records) == 0:
                    break
        return blocks_list
