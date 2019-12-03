"""
Function:
    随机生成迷宫
Arithmetic：
    Randomized Prim's algorithm
    Recursive backtracking
"""
import pygame
import cfg
import random
from modules.misc import *

'''一个游戏地图块'''


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


'''随机生成迷宫类'''


class RandomMaze(object):
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
        # ----生成全是墙的迷宫
        blocks_list = [[Block([col, row], block_size, border_size) for col in range(maze_size[1])] for row in
                       range(maze_size[0])]
        # ----将一个单元格加入栈 标记访问
        block_now = blocks_list[0][0]
        block_now.is_visited = True
        records = [block_now]
        # ----当栈不空时
        while records:
            # ---从堆栈中弹出一个单元格，使其成为当前单元格
            block_now = records.pop()
            # ---检查当前单元格的相邻单元 记录未被访问过的
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
            # ---存在未被访问的邻格
            if check:
                # ---当前单元格入栈
                records.append(block_now)
                # ---随机选择邻格
                move_direction = random.choice(check)
                for index, item in enumerate(check_list):
                    if item['direction'] == move_direction:
                        # ----拆除墙
                        blocks_list[r][c].has_walls[index] = False
                        blocks_list[item['coordinate'][0]][item['coordinate'][1]].has_walls[item['index']] = False
                        # ----标记访问
                        blocks_list[item['coordinate'][0]][item['coordinate'][1]].is_visited = True
                        # ----入栈
                        records.append(blocks_list[item['coordinate'][0]][item['coordinate'][1]])
                        break
        return blocks_list

    @staticmethod
    def createMaze_Prim(maze_size, block_size, border_size):
        # ----生成全是墙的迷宫
        blocks_list = [[Block([col, row], block_size, border_size) for col in range(maze_size[1])] for row in
                       range(maze_size[0])]
        # ----将一个单元格加入列表
        block_now = blocks_list[0][0]
        records = [block_now]
        # ----当列表不空时
        while records:
            # ---随机取出一个单元格
            block_now = random.choice(records)
            # ---标记访问 加入迷宫
            block_now.is_visited = True
            # ---从列表中移除这个单元格
            records.remove(block_now)
            # ---检查相邻单元格 上下左右
            check = []
            c, r = block_now.coordinate[0], block_now.coordinate[1]
            check_list = [
                {'check': r > 0, 'coordinate': (r - 1, c), 'direction': 'Up', 'index': 1},
                {'check': r < maze_size[0] - 1, 'coordinate': (r + 1, c), 'direction': 'Down', 'index': 0},
                {'check': c > 0, 'coordinate': (r, c - 1), 'direction': 'Left', 'index': 3},
                {'check': c < maze_size[1] - 1, 'coordinate': (r, c + 1), 'direction': 'Right', 'index': 2}
            ]
            for item in check_list:
                # 如果单元格合法
                if item['check']:
                    # 如果该相邻单元格在已在迷宫中，记录该单元格
                    if blocks_list[item['coordinate'][0]][item['coordinate'][1]].is_visited:
                        check.append(item['direction'])
                    else:
                        # 否则 若该单元格不在列表中，加入列表
                        if not blocks_list[item['coordinate'][0]][item['coordinate'][1]] in records:
                            records.append(blocks_list[item['coordinate'][0]][item['coordinate'][1]])
            if check:
                # 从记录的相邻单元格中随机随机选择一个单元格 将中间的墙拆除
                move_direction = random.choice(check)
                for index, item in enumerate(check_list):
                    if item['direction'] == move_direction:
                        blocks_list[r][c].has_walls[index] = False
                        blocks_list[item['coordinate'][0]][item['coordinate'][1]].has_walls[item['index']] = False
                        break
        return blocks_list
