import cfg
import pygame
from modules.misc import *

'''主函数'''

cfg.FPS = 100


def main(cfg):
    # 初始化
    pygame.init()
    pygame.font.init()
    screen = pygame.display.set_mode(cfg.SCREENSIZE)
    pygame.display.set_caption('Maze')
    font = pygame.font.SysFont('ComicSansMS', 15)
    modes = {'start': 'game_start', 'switch': 'game_switch', 'end': 'game_end'}
    # 开始界面
    Interface(screen, cfg, modes['start'])
    setting(screen,cfg)
    # 记录关卡数
    num_levels = 0
    # 记录
    screen.fill((255, 255, 255))
    pygame.display.update()
    while True:
        for event in pygame.event.get():
            pass
    pygame.quit()


if __name__ == '__main__':
    main(cfg)
