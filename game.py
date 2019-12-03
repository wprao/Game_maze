"""
Function:
    主函数
"""

import cfg
import sys
import pygame
from modules.misc import *
from modules.Sprites import *
from modules.mazes import *
from modules.pathfinding import *

'''主函数'''


def main(cfg):
    # ----初始化
    pygame.init()
    pygame.font.init()
    screen = pygame.display.set_mode(cfg.SCREENSIZE)
    pygame.display.set_caption('Maze')

    # ----字体
    font = pygame.font.SysFont(cfg.FONT, 15)
    font_button = pygame.font.SysFont(cfg.FONT, 15)  # 按钮字体
    font_button.set_underline(True)  # 按钮字体开启下划线
    font_focus = pygame.font.SysFont(cfg.FONT, 25)  # 按钮焦点字体
    # ----三个界面
    modes = {'start': 'game_start', 'switch': 'game_switch', 'end': 'game_end'}
    # ----开始界面
    choice = Interface(screen, cfg, modes['start'])
    # start or restart
    while True:
        # ---退出游戏
        if not choice:
            pygame.quit()
            sys.exit(-1)
        # ---设置界面 返回迷宫生成算法
        arithmetic = setting(screen, cfg)
        # ---记录关卡数
        num_levels = 0

        # ---关卡循环切换
        while True:
            num_levels += 1
            clock = pygame.time.Clock()
            screen = pygame.display.set_mode(cfg.SCREENSIZE)
            # --随机生成关卡地图
            maze_now = RandomMaze(cfg.MAZESIZE, cfg.BLOCKSIZE, cfg.BORDERSIZE, arithmetic, cfg.STARTPOINT,
                                  cfg.DESTINATION)
            # --生成hero
            start = [cfg.STARTPOINT[1], cfg.STARTPOINT[0]]
            hero_now = Hero(cfg.HEROPICPATH, start, cfg.BLOCKSIZE, cfg.BORDERSIZE)
            # --统计步数
            num_steps = 0
            # --记录路径
            move_records = []
            # --寻路功能按钮：显示路径 直接通关
            path_finding = ["Lost your way ?(A*)", "Lost your way ?(BFS)", "Too lazy ?"]
            path_n = 0

            # --预先获取位置
            rect = pygame.Rect(10, 10, font.size('Level Done: %d' % num_levels)[0],
                               font.size('Level Done: %d' % num_levels)[1])
            button = Label_ce(screen, font_button, path_finding[path_n], cfg.HIGHLIGHT,
                              (cfg.SCREENSIZE[0] - font_button.size(path_finding[0])[0], rect.centery))
            # --关卡内主循环
            while True:
                dt = clock.tick(cfg.FPS)
                screen.fill((255, 255, 255))
                is_move = False

                # ----寻找路径
                if path_n !=2:
                    guide, searched = A_Star(maze_now, hero_now.coordinate, cfg.DESTINATION)
                else:
                    guide, searched = BFS(maze_now, hero_now.coordinate, cfg.DESTINATION)

                # ----显示移动路径
                for move in move_records:
                    pygame.draw.circle(screen, cfg.HIGHLIGHT, move, 2)

                # ----显示路径
                if path_n != 0:
                    for move in searched:
                        pygame.draw.circle(screen, cfg.LINE, move, 2)
                    for move in guide:
                        pygame.draw.circle(screen, cfg.FOREGROUND, move, 2)

                # ----显示一些信息
                Label_co(screen, font, 'Level Done: %d' % num_levels, cfg.HIGHLIGHT, (10, 10))
                Label_co(screen, font, 'Used Steps: %s' % num_steps, cfg.HIGHLIGHT, (cfg.SCREENSIZE[0] // 4 + 10, 10))
                Label_co(screen, font, 'Min Cost: %s' % (len(guide) - 1), cfg.HIGHLIGHT,
                         (cfg.SCREENSIZE[0] // 2 + 10, 10))
                Label_co(screen, font, 'S: your starting point    D: your destination', cfg.HIGHLIGHT,
                         (10, cfg.SCREENSIZE[1] - font.size('')[1] - 10))

                # ----显示按钮
                if button.collidepoint(pygame.mouse.get_pos()):
                    button = Label_ce(screen, font_focus, path_finding[path_n], cfg.HIGHLIGHT,
                                      (cfg.SCREENSIZE[0] - font_button.size(path_finding[0])[0], rect.centery))
                else:
                    button = Label_ce(screen, font_button, path_finding[path_n], cfg.HIGHLIGHT,
                                      (cfg.SCREENSIZE[0] - font_button.size(path_finding[0])[0], rect.centery))

                # ----事件响应 ↑↓←→控制hero
                for event in pygame.event.get():
                    # 退出
                    if event.type == pygame.QUIT:
                        pygame.quit()
                        sys.exit(-1)
                    # 点击事件
                    elif event.type == pygame.MOUSEBUTTONDOWN:
                        if path_n != 2:
                            path_n += 1
                        else:
                            move_records += guide
                            hero_now.coordinate[0] = cfg.DESTINATION[1]
                            hero_now.coordinate[1] = cfg.DESTINATION[0]
                    # 键盘事件
                    elif event.type == pygame.KEYDOWN:
                        # 判断是否移动
                        if event.key == pygame.K_UP:
                            is_move = hero_now.move('Up', maze_now)
                        elif event.key == pygame.K_DOWN:
                            is_move = hero_now.move('Down', maze_now)
                        elif event.key == pygame.K_LEFT:
                            is_move = hero_now.move('Left', maze_now)
                        elif event.key == pygame.K_RIGHT:
                            is_move = hero_now.move('Right', maze_now)
                num_steps += int(is_move)

                # 添加移动记录
                if is_move:
                    left, top = hero_now.coordinate[0] * cfg.BLOCKSIZE + cfg.BORDERSIZE[0], hero_now.coordinate[
                        1] * cfg.BLOCKSIZE + cfg.BORDERSIZE[1]
                    move_records.append((left + cfg.BLOCKSIZE // 2, top + cfg.BLOCKSIZE // 2))

                hero_now.draw(screen)
                maze_now.draw(screen)

                # ----判断游戏是否胜利
                if (hero_now.coordinate[0] == cfg.DESTINATION[1]) and (hero_now.coordinate[1] == cfg.DESTINATION[0]):
                    break
                pygame.display.update()

            # --关卡切换
            choice = Interface(screen, cfg, modes['switch'])
            if not choice:
                break
        choice = Interface(screen, cfg, modes['end'])


if __name__ == '__main__':
    # 读入配置
    cfgs = cfg.read_cfg()
    cfg.MAZESIZE = cfgs['MAZESIZE']
    cfg.STARTPOINT = cfgs['STARTPOINT']
    cfg.DESTINATION = cfgs['DESTINATION']
    main(cfg)
