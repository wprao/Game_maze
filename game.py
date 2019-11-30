import cfg
import sys
import pygame
from modules.misc import *
from modules.Sprites import *
from modules.mazes import *
from modules.pathfinding import *

'''主函数'''


def main(cfg):
    # 初始化
    pygame.init()
    pygame.font.init()
    screen = pygame.display.set_mode(cfg.SCREENSIZE)
    pygame.display.set_caption('Maze')
    font = pygame.font.SysFont(cfg.FONT, 15)
    font_button = pygame.font.SysFont(cfg.FONT, 15)
    font_button.set_underline(True)
    font_focus = pygame.font.SysFont(cfg.FONT, 25)
    modes = {'start': 'game_start', 'switch': 'game_switch', 'end': 'game_end'}
    # 开始界面
    choice = Interface(screen, cfg, modes['start'])
    # start or restart
    while True:
        if not choice:
            pygame.quit()
            sys.exit(-1)
        # 设置界面
        arithmetic = setting(screen, cfg)
        # 记录关卡数
        num_levels = 0
        # 记录最少用了多少步通关
        best_scores = 'None'
        # 关卡循环切换
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
            # --记录步数
            move_records = []
            # --寻路功能
            path_finding = ["Lost your way ?", "Too lazy ?"]
            path_n = 0
            guide = []
            rect = pygame.Rect(10, 10, font.size('Level Done: %d' % num_levels)[0],
                               font.size('Level Done: %d' % num_levels)[1])
            button = Label_ce(screen, font_button, path_finding[path_n], cfg.HIGHLIGHT,
                              (cfg.SCREENSIZE[0] - font_button.size(path_finding[0])[0], rect.centery))
            # --关卡内主循环
            while True:
                dt = clock.tick(cfg.FPS)
                screen.fill((255, 255, 255))
                is_move = False
                if path_n==1:
                    for move in guide:
                        pygame.draw.circle(screen, cfg.FOREGROUND, move, 2)
                for move in move_records:
                    pygame.draw.circle(screen, cfg.HIGHLIGHT, move, 2)
                guide = A_Star(maze_now, hero_now.coordinate, cfg.DESTINATION)
                # ----显示一些信息
                Label_co(screen, font, 'Level Done: %d' % num_levels, cfg.HIGHLIGHT, (10, 10))
                Label_co(screen, font, 'Used Steps: %s' % num_steps, cfg.HIGHLIGHT, (cfg.SCREENSIZE[0] // 4 + 10, 10))
                Label_co(screen, font, 'Min Cost: %s' % (len(guide)-1), cfg.HIGHLIGHT, (cfg.SCREENSIZE[0] // 2 + 10, 10))
                Label_co(screen, font, 'S: your starting point    D: your destination', cfg.HIGHLIGHT,
                         (10, cfg.SCREENSIZE[1] - font.size('')[1] - 10))
                if button.collidepoint(pygame.mouse.get_pos()):
                    button = Label_ce(screen, font_focus, path_finding[path_n], cfg.HIGHLIGHT,
                                      (cfg.SCREENSIZE[0] - font_button.size(path_finding[0])[0], rect.centery))
                else:
                    button = Label_ce(screen, font_button, path_finding[path_n], cfg.HIGHLIGHT,
                                      (cfg.SCREENSIZE[0] - font_button.size(path_finding[0])[0], rect.centery))
                # ----↑↓←→控制hero
                for event in pygame.event.get():
                    if event.type == pygame.QUIT:
                        pygame.quit()
                        sys.exit(-1)
                    elif event.type == pygame.MOUSEBUTTONDOWN:
                        if path_n == 0:
                            path_n = 1
                        else:
                            move_records += guide
                            hero_now.coordinate[0] = cfg.DESTINATION[1]
                            hero_now.coordinate[1] = cfg.DESTINATION[0]
                    elif event.type == pygame.KEYDOWN:
                        if event.key == pygame.K_UP:
                            is_move = hero_now.move('up', maze_now)
                        elif event.key == pygame.K_DOWN:
                            is_move = hero_now.move('down', maze_now)
                        elif event.key == pygame.K_LEFT:
                            is_move = hero_now.move('left', maze_now)
                        elif event.key == pygame.K_RIGHT:
                            is_move = hero_now.move('right', maze_now)
                num_steps += int(is_move)
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
            # --更新最优成绩
            if best_scores == 'None':
                best_scores = num_steps
            else:
                if best_scores > num_steps:
                    best_scores = num_steps
            # --关卡切换
            choice = Interface(screen, cfg, modes['switch'])
            if not choice:
                break
        choice = Interface(screen, cfg, modes['end'])


if __name__ == '__main__':
    cfgs = cfg.read_cfg()
    cfg.MAZESIZE = cfgs['MAZESIZE']
    cfg.STARTPOINT = cfgs['STARTPOINT']
    cfg.DESTINATION = cfgs['DESTINATION']
    main(cfg)
