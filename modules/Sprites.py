"""
Function:
    定义游戏精灵类
"""
import pygame

'''定义hero'''


class Hero(pygame.sprite.Sprite):
    def __init__(self, imagepath, coordinate, block_size, border_size, **kwargs):
        pygame.sprite.Sprite.__init__(self)
        self.image = pygame.image.load(imagepath)
        self.image = pygame.transform.scale(self.image, (block_size, block_size))
        self.rect = self.image.get_rect()
        self.rect.left, self.rect.top = coordinate[0] * block_size + border_size[0], coordinate[1] * block_size + \
                                        border_size[1]
        self.coordinate = coordinate
        self.block_size = block_size
        self.border_size = border_size

    '''移动'''

    def move(self, direction, maze):
        blocks_list = maze.blocks_list
        # 上下左右对应坐标的加减
        directions = {'Up': (0, -1), 'Down': (0, 1), 'Left': (-1, 0), 'Right': (1, 0)}
        for index, key in enumerate(directions.keys()):
            if direction == key:
                if blocks_list[self.coordinate[1]][self.coordinate[0]].has_walls[index]:
                    return False
                else:
                    self.coordinate[0] += directions[key][0]
                    self.coordinate[1] += directions[key][1]
                    return True

    '''绑定到屏幕'''

    def draw(self, screen):
        self.rect.left, self.rect.top = self.coordinate[0] * self.block_size + self.border_size[0], self.coordinate[
            1] * self.block_size + self.border_size[1]
        screen.blit(self.image, self.rect)
