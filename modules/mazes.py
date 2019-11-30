"""
Function:
    随机生成迷宫
"""
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
        if arithmetic == 'Prim':
            self.blocks_list = RandomMaze.createMaze_Prim(maze_size, block_size, border_size)
        else:
            self.blocks_list = RandomMaze.createMaze_DFS(maze_size, block_size, border_size)
        # self.blocks_list = RandomMaze.createMaze_DFS(maze_size, block_size, border_size)
        self.font = pygame.font.SysFont(cfg.FONT, 12)

    '''画到屏幕上'''

    def draw(self, screen):
        for row in range(self.maze_size[0]):
            for col in range(self.maze_size[1]):
                self.blocks_list[row][col].draw(screen)
        # 起点和终点标志
        Label_ce(screen, self.font, 'S', (255, 0, 0),
                 (self.starting_point[1] * self.block_size + self.border_size[0] + 8, self.starting_point[
                     0] * self.block_size + self.border_size[1] + 8))
        Label_ce(screen, self.font, 'D', (255, 0, 0),
                 (self.destination[1] * self.block_size + self.border_size[0] + 8, self.destination[
                     0] * self.block_size + self.border_size[1] + 8))

    '''创建迷宫'''

    @staticmethod
    def createMaze_DFS(maze_size, block_size, border_size):
        blocks_list = [[Block([col, row], block_size, border_size) for col in range(maze_size[1])] for row in
                       range(maze_size[0])]
        block_now = blocks_list[0][0]
        records = [block_now]
        while records:
            if not block_now.is_visited:
                records.append(block_now)
                block_now.is_visited = True
            check = []
            c, r = block_now.coordinate[0], block_now.coordinate[1]
            check_list = [
                {'check': r > 0, 'coordinate': (r - 1, c), 'direction': 'Up', 'index': 1},
                {'check': r < maze_size[0] - 1, 'coordinate': (r + 1, c), 'direction': 'Down', 'index': 0},
                {'check': c > 0, 'coordinate': (r, c - 1), 'direction': 'Left', 'index': 3},
                {'check': c < maze_size[1] - 1, 'coordinate': (r, c + 1), 'direction': 'Right', 'index': 2}
            ]
            for item in check_list:
                if item['check'] and not blocks_list[item['coordinate'][0]][item['coordinate'][1]].is_visited:
                    check.append(item['direction'])
            if check:
                records.append(block_now)
                move_direction = random.choice(check)
                for index, item in enumerate(check_list):
                    if item['direction'] == move_direction:
                        blocks_list[r][c].has_walls[index] = False
                        blocks_list[item['coordinate'][0]][item['coordinate'][1]].has_walls[item['index']] = False
                        block_now=blocks_list[item['coordinate'][0]][item['coordinate'][1]]
                        break
            else:
                block_now = records.pop()
        return blocks_list

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
            c, r = block_now.coordinate[0], block_now.coordinate[1]
            check_list = [
                {'check': r > 0, 'coordinate': (r - 1, c), 'direction': 'Up', 'index': 1},
                {'check': r < maze_size[0] - 1, 'coordinate': (r + 1, c), 'direction': 'Down', 'index': 0},
                {'check': c > 0, 'coordinate': (r, c - 1), 'direction': 'Left', 'index': 3},
                {'check': c < maze_size[1] - 1, 'coordinate': (r, c + 1), 'direction': 'Right', 'index': 2}
            ]
            for item in check_list:
                if item['check']:
                    if blocks_list[item['coordinate'][0]][item['coordinate'][1]].is_visited:
                        check.append(item['direction'])
                    else:
                        if not blocks_list[item['coordinate'][0]][item['coordinate'][1]] in records:
                            records.append(blocks_list[item['coordinate'][0]][item['coordinate'][1]])
            if check:
                move_direction = random.choice(check)
                for index, item in enumerate(check_list):
                    if item['direction'] == move_direction:
                        blocks_list[r][c].has_walls[index] = False
                        blocks_list[item['coordinate'][0]][item['coordinate'][1]].has_walls[item['index']] = False
                        break
        return blocks_list
