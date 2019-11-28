import sys
import pygame
from pygame.locals import *
import pygame, pygame.font, pygame.event, pygame.draw, string
from tkinter import simpledialog


def isvisited(screen, position, color=(255, 0, 0)):
    pygame.draw.circle(screen, color, position, 2)


def showText(screen, font, text, color, position):
    text_render = font.render(text, True, color)  # 文本样式
    rect = text_render.get_rect()  # 文本位置
    rect.left, rect.top = position
    screen.blit(text_render, rect)
    return rect.right


def Button(screen, position, text, font, buttoncolor=(0, 0, 0), textcolor=(255, 255, 255),
           bwidth=200, bheigh=50):
    left, top = position
    # 画一个矩形
    pygame.draw.rect(screen, buttoncolor, (left, top, bwidth, bheigh))
    text_render = font.render(text, True, textcolor)
    rect = text_render.get_rect()
    rect.centerx, rect.centery = left + bwidth / 2, top + bheigh / 2
    return screen.blit(text_render, rect)

# http://www.pygame.org/pcr/inputbox/
def InputBox(screen, position, question, font, boxcolor=(0, 0, 0),
             textcolor=(255, 255, 255),
             bwidth=200, bheigh=50):
    current_string = []
    Button(screen, position, question, font, boxcolor, textcolor, bwidth, bheigh)
    pygame.display.update()
    while True:
        while True:
            for event in pygame.event.get():
                if event.type==pygame.QUIT:
                    pygame.quit()
                    sys.exit(-1)
                if event.type == KEYDOWN:
                    inkey = event.key;
                    if inkey == K_BACKSPACE:
                        current_string = current_string[0:-1]
                    elif inkey == K_RETURN:
                        break
                    elif inkey <= 127:
                        current_string.append(chr(inkey))
                    else:
                        pass
                    Button(screen, position, question + ':' + "".join(current_string), font, boxcolor, textcolor,
                           bwidth, bheigh)
                    pygame.display.update()
                else:
                    pass
    return "".join(current_string)


def Interface(screen, cfg, mode='game start'):
    pygame.display.set_mode(cfg.SCREENSIZE)
    font = pygame.font.SysFont('Comic Sans MS', 30)
    if mode == 'game_start':
        clock = pygame.time.Clock()
        while (True):
            screen.fill((255, 255, 255))
            showText(screen, pygame.font.SysFont('Consolas', 90), 'M A Z E', (255, 0, 0),
                     ((cfg.SCREENSIZE[0] - 350) // 2, cfg.SCREENSIZE[1] // 6))
            button_start = Button(screen, ((cfg.SCREENSIZE[0] - 200) // 2, cfg.SCREENSIZE[1] // 3), 'START', font)
            button_quit = Button(screen, ((cfg.SCREENSIZE[0] - 200) // 2, cfg.SCREENSIZE[1] - cfg.SCREENSIZE[1] // 3),
                                 'QUIT', font)
            # button_setting = InputBox(screen, ((cfg.SCREENSIZE[0] - 200) // 2, cfg.SCREENSIZE[1] // 2), 'SETTING', font)

            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    pygame.quit()
                    sys.exit(-1)
                elif event.type == pygame.MOUSEBUTTONDOWN:
                    if button_start.collidepoint(pygame.mouse.get_pos()):
                        return True
                    elif button_quit.collidepoint(pygame.mouse.get_pos()):
                        pygame.quit()
                        sys.exit(-1)
            pygame.display.update()
            clock.tick(cfg.FPS)
    elif mode == 'game_switch':
        clock = pygame.time.Clock()
        while True:
            screen.fill((255, 255, 255))
            button_start = Button(screen, ((cfg.SCREENSIZE[0] - 200) // 2, cfg.SCREENSIZE[1] // 3), 'NEXT',
                                  font)
            button_quit = Button(screen, ((cfg.SCREENSIZE[0] - 200) // 2, cfg.SCREENSIZE[1] // 2), 'QUIT',
                                 font)
            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    pygame.quit()
                    sys.exit(-1)
                elif event.type == pygame.MOUSEBUTTONDOWN:
                    if button_start.collidepoint(pygame.mouse.get_pos()):
                        return True
                    elif button_quit.collidepoint(pygame.mouse.get_pos()):
                        pygame.quit()
                        sys.exit(-1)
            pygame.display.update()
            clock.tick(cfg.FPS)
    elif mode == 'game_end':
        clock = pygame.time.Clock()
        while True:
            screen.fill((255, 255, 255))
            button_start = Button(screen, ((cfg.SCREENSIZE[0] - 200) // 2, cfg.SCREENSIZE[1] // 3), 'RESTART', font)
            button_quit = Button(screen, ((cfg.SCREENSIZE[0] - 200) // 2, cfg.SCREENSIZE[1] // 2), 'QUIT', font)
            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    pygame.quit()
                    sys.exit(-1)
                elif event.type == pygame.MOUSEBUTTONDOWN:
                    if button_start.collidepoint(pygame.mouse.get_pos()):
                        return True
                    elif button_quit.collidepoint(pygame.mouse.get_pos()):
                        pygame.quit()
                        sys.exit(-1)
            pygame.display.update()
            clock.tick(cfg.FPS)
    else:
        raise ValueError('Interface.mode unsupport <%s>...' % mode)
