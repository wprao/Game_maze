import cfg
import pygame
from modules.misc import *

'''主函数'''


def main(cfg):
    # 初始化
    pygame.init()
    pygame.font.init()
    screen = pygame.display.set_mode(cfg.SCREENSIZE)
    pygame.display.set_caption('Maze')
    font = pygame.font.SysFont('Consolas', 15)
    # 开始界面
    Interface(screen, cfg, 'game start')
    # 记录关卡数
    num_levels=0
    # 记录
    pygame.quit()


if __name__ == '__main__':
    main(cfg)
