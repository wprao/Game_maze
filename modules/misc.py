"""
Fucntion:
    其他必要模块：Label，setting界面，其他界面
"""

import re
import sys
import pygame
from pygame.locals import *
import pygame.font
import pygame.event
import pygame.draw


def read_cfg(cfg):
    cfgs = cfg.read_cfg()
    cfg.MAZESIZE = cfgs['MAZESIZE']
    cfg.STARTPOINT = cfgs['STARTPOINT']
    cfg.DESTINATION = cfgs['DESTINATION']


'''Label: 在指定位置（中心）显示文字'''


def Label_ce(screen, font, text, color, position):
    text_render = font.render(text, True, color)  # 文本样式
    rect = text_render.get_rect()  # 文本位置
    rect.centerx, rect.centery = position
    return screen.blit(text_render, rect)


'''Label: 在指定位置（左上角）显示文字'''


def Label_co(screen, font, text, color, position):
    text_render = font.render(text, True, color)  # 文本样式
    rect = text_render.get_rect()  # 文本位置
    rect.left, rect.top = position
    return screen.blit(text_render, rect)


'''setting: 检查输入设置文本格式是否正确'''


def check_setted(cfg):
    setted = [True, False, False, False, False]
    # ----类型转换为字符串
    for key in cfg.keys():
        cfg[key] = str(cfg[key])
    # ----Rows是否为数字
    if cfg['Rows'].isdigit():
        # ----转换为数字
        cfg['Rows'] = int(cfg['Rows'])
        # ----检查数字范围（0，35]
        if 0 < cfg['Rows'] <= 35:
            setted[1] = True
    # ----Cols是否为数字
    if cfg['Cols'].isdigit():
        # ----转换为数字
        cfg['Cols'] = int(cfg['Cols'])
        # ----检查数字范围(0,50]
        if 0 < cfg['Cols'] <= 50:
            setted[2] = True
    # ----正则表达式 匹配起点，终点输入格式
    pattern = re.compile('^\[(\d{1,})[，*,*\s]*(\d{1,})\]$')
    g = pattern.match(cfg['Starting point'])
    if g:
        x, y = g.group(1), g.group(2)
        cfg['Starting point'] = [int(x), int(y)]
        if setted[1] and setted[2] and 0 < cfg['Starting point'][0] <= cfg['Rows'] and 0 < cfg['Starting point'][1] <= \
                cfg['Cols']:
            setted[3] = True
    g = pattern.match(cfg['Destination'])
    if g:
        x, y = g.group(1), g.group(2)
        cfg['Destination'] = [int(x), int(y)]
        if setted[1] and setted[2] and 0 < cfg['Destination'][0] <= cfg['Rows'] and 0 < cfg['Destination'][1] <= cfg[
            'Cols']:
            setted[4] = True
    return setted


'''setting: 输入框显示'''


# 字体，是否为焦点输入框，输入问题，输入回答，输入提示，字体颜色，输入框位置，输入框最大宽度
def InputBox(screen, font, focus, question, ans, hint, color, position, max):
    # ----焦点输入框设置字体斜体
    font.set_italic(focus)
    # ----根据本身宽度、最大宽度求空格数
    width, height = font.size(question + ans + hint)
    blank = (max - position[0] - width) // 2 // font.size(' ')[0]
    left = (max - position[0] - width - blank * font.size(' ')[0]) // font.size(' ')[0]
    # ----输入问题显示
    rect = Label_co(screen, font, question, color, position)
    # ----输入回答显示
    x, y = rect.left + rect.width, rect.top  # 根据输入问题位置求显示位置
    font.set_underline(focus)  # 焦点输入框输入回答位置设置下划线
    rect2 = Label_co(screen, font, ' ' * blank + ans + ' ' * left, color, (x, y))
    font.set_underline(False)
    # ----输入提示显示
    Label_co(screen, font, hint, color, (rect2.left + rect2.width, y))
    font.set_italic(False)
    return pygame.Rect(rect.left, rect.top, max - position[0], rect.height)


'''setting: 界面设置及其响应事件（包含按钮、输入框）'''


def setting(screen, cfg):
    read_cfg(cfg)
    # ----字体样式
    font_title = pygame.font.SysFont(cfg.FONT, 80)  # 标题字体
    font = pygame.font.SysFont(cfg.FONT2, 45)  # 输入框字体
    font_warn = pygame.font.SysFont(cfg.FONT2, 20)  # 提示字体
    font_start = pygame.font.SysFont(cfg.FONT, 70)  # 按钮字体
    font_start.set_underline(True)  # 按钮字体开启下划线
    font_start_focus = pygame.font.SysFont(cfg.FONT, 85)  # 按钮焦点字体

    # ----设置
    cfg_now = {'Rows': cfg.MAZESIZE[0], 'Cols': cfg.MAZESIZE[1], 'Starting point': cfg.STARTPOINT,
               'Destination': cfg.DESTINATION}
    # ----设置检查
    setted = check_setted(cfg_now)

    # ----设置正误相关提示
    warnings = {'Correct': 'Correct settings', 'Incorrect': 'Incorrect settings'}

    # ----输入框相关参数：行数、列数、起点、终点
    focus = ['title', 'Rows', 'Cols', 'Starting point', 'Destination']  # 标题 输入问题
    hint = {'Rows': '(0<rows<=35)', 'Cols': '(0 < cols <= 50)', 'Starting point': ' ', 'Destination': ' '}  # 输入提示
    color = {'True': cfg.HIGHLIGHT, 'False': cfg.FOREGROUND}

    # ----焦点输入框下标 默认第一个
    focus_now = 1

    # ----按钮：Randomized Prim's algorithm、Recursive backtracking
    buttons = {'Prim': Label_ce(screen, font_start, 'Prim', cfg.FOREGROUND,
                                (cfg.SCREENSIZE[0] // 4, cfg.SCREENSIZE[1] - font_start.size('')[1] // 2)),
               'DFS': Label_ce(screen, font_start, 'DFS', cfg.FOREGROUND,
                               (cfg.SCREENSIZE[0] - cfg.SCREENSIZE[0] // 4,
                                cfg.SCREENSIZE[1] - font_start.size('')[1] // 2))}

    # ----setting主循环
    while True:
        screen.fill(cfg.BACKGROUND)
        # ----绘制标题
        labels = {'title': Label_co(screen, font_title, 'Setting:', cfg.FOREGROUND, (10, 0)),
                  'Rows': None, 'Cols': None, 'Starting point': None, 'Destination': None}
        pygame.draw.line(screen, cfg.LINE, (0, labels['title'].top + labels['title'].height - 20),
                         # (labels['title'].left + labels['title'].width + 400,
                         (cfg.SCREENSIZE[0], labels['title'].top + labels['title'].height - 20))  # 分割线

        # ----绘制输入框（区分焦点输入框）
        for i in range(1, 5):
            labels[focus[i]] = InputBox(screen, font, i == focus_now, focus[i] + ': ', str(cfg_now[focus[i]]),
                                        hint[focus[i]], color[str(i == focus_now)],
                                        (20, labels[focus[i - 1]].top + labels[focus[i - 1]].height + 30),
                                        cfg.SCREENSIZE[0])

        # ----显示提醒
        if setted.count(True) == 5:  # 设置正确
            warn = warnings['Correct']
        else:
            warn = warnings['Incorrect']
        warning = Label_co(screen, font_warn, '· Tips: ' + warn, cfg.HIGHLIGHT,
                           (20, cfg.SCREENSIZE[1] - font_start_focus.size('')[1] - 30))
        pygame.draw.line(screen, cfg.LINE, (0, warning.top + warning.height),
                         (cfg.SCREENSIZE[0], warning.top + warning.height))  # 分割线

        # ----按钮 区分设置正确与否 区分焦点
        for key in buttons.keys():
            if buttons[key].collidepoint(pygame.mouse.get_pos()) and warn == warnings['Correct']:
                buttons[key] = Label_ce(screen, font_start_focus, key, cfg.FOREGROUND,
                                        (buttons[key].centerx, buttons[key].centery));
            else:
                buttons[key] = Label_ce(screen, font_start, key, cfg.FOREGROUND,
                                        (buttons[key].centerx, buttons[key].centery));

        # ----当前焦点输入框的内容
        current_string = list(str(cfg_now[focus[focus_now]]))

        # ----事件响应
        for event in pygame.event.get():
            # 退出游戏
            if event.type == pygame.QUIT:
                pygame.quit()
                sys.exit(-1)
            # 鼠标点击
            elif event.type == pygame.MOUSEBUTTONDOWN:
                # 点击按钮 检查按钮及是否可按（设置是否正确）
                for key in buttons.keys():
                    if buttons[key].collidepoint(pygame.mouse.get_pos()) and warn == warnings['Correct']:
                        # 正确->修改配置
                        cfg.MAZESIZE = [cfg_now['Rows'], cfg_now['Cols']]
                        cfg.STARTPOINT = cfg_now['Starting point']
                        cfg.DESTINATION = cfg_now['Destination']
                        cfg.BORDERSIZE = (
                            (cfg.SCREENSIZE[0] - cfg.MAZESIZE[1] * cfg.BLOCKSIZE) // 2,
                            (cfg.SCREENSIZE[1] - cfg.MAZESIZE[0] * cfg.BLOCKSIZE) // 2)
                        cfg.write_cfg()  # 将新配置写入配置文件
                        cfg.STARTPOINT = [cfg_now['Starting point'][0] - 1, cfg_now['Starting point'][1] - 1]
                        cfg.DESTINATION = [cfg_now['Destination'][0] - 1, cfg_now['Destination'][1] - 1]
                        return key
                # 点击标签
                for key in labels.keys():
                    if labels[key].collidepoint(pygame.mouse.get_pos()) and key != 'title':
                        focus_now = focus.index(key)
            # 键盘输入
            elif event.type == KEYDOWN:
                inkey = event.key
                if inkey == K_BACKSPACE:  # 撤销
                    current_string = current_string[0:-1]
                    cfg_now[focus[focus_now]] = ''.join(current_string)  # 更新字符串
                elif inkey == K_RETURN or inkey == K_RIGHT or inkey == K_DOWN:  # 下个输入框
                    if focus_now < 4:
                        focus_now = focus_now + 1
                elif inkey == K_LEFT or inkey == K_UP:  # 上个输入框
                    if focus_now > 1:
                        focus_now = focus_now - 1
                elif inkey <= 127:  # 输入字符
                    current_string.append(chr(inkey))
                    cfg_now[focus[focus_now]] = ''.join(current_string)  # 更新字符串
            else:
                pass
            # 设置更新
            setted = check_setted(cfg_now)
        # 界面更新
        pygame.display.update()


'''Interface: 其他界面设置及其响应事件（包含按钮）'''


def Interface(screen, cfg, mode='game_start', title='Maze'):
    # ----字体样式
    font_title = pygame.font.SysFont(cfg.FONT, 120)  # 标题字体
    font = pygame.font.SysFont(cfg.FONT, 55)  # 按钮字体
    font.set_underline(True)  # 按钮字体开启下划线
    font_focus = pygame.font.SysFont(cfg.FONT, 100)  # 焦点按钮字体
    # ----按钮样式
    label_title = {'font': font_title, 'font_focus': font_title, 'text': title, 'color': cfg.HIGHLIGHT,
                   'position': ((cfg.SCREENSIZE[0]) // 2, cfg.SCREENSIZE[1] // 4)}
    label_continue = {'font': font, 'font_focus': font_focus, 'text': 'Start', 'color': cfg.FOREGROUND,
                      'position': ((cfg.SCREENSIZE[0]) // 2, cfg.SCREENSIZE[1] // 2)}
    label_quit = {'font': font, 'font_focus': font_focus, 'text': 'Quit', 'color': cfg.FOREGROUND,
                  'position': ((cfg.SCREENSIZE[0]) // 2, cfg.SCREENSIZE[1] - cfg.SCREENSIZE[1] // 3)}
    label_format = {'title': label_title, 'continue': label_continue, 'quit': label_quit}
    if mode == 'game_switch':
        label_continue['text'] = 'Next'
    elif mode == 'game_end':
        label_continue['text'] = 'Restart'

    # ----按钮
    buttons = {'title': None, 'continue': None, 'quit': None}

    clock = pygame.time.Clock()
    screen.fill(cfg.BACKGROUND)

    for key in buttons.keys():
        buttons[key] = Label_ce(screen, label_format[key]['font'], label_format[key]['text'],
                                label_format[key]['color'],
                                label_format[key]['position'])
    pygame.draw.line(screen, cfg.LINE,
                     (buttons['title'].left - 100, buttons['title'].top + buttons['title'].height - 40), (
                         buttons['title'].left + buttons['title'].width + 100,
                         buttons['title'].top + buttons['title'].height - 40))

    # ----Logo图片
    image = pygame.image.load(cfg.HEROPICPATH)
    image = pygame.transform.scale(image, (50, 50))
    rect = image.get_rect()
    rect.centerx, rect.centery = buttons['title'].centerx + buttons['title'].width // 2 + 25, buttons[
        'title'].centery + 30
    screen.blit(image, rect)

    # ----界面主循环
    while True:
        screen.fill(cfg.BACKGROUND)
        # 绘制按钮 区分焦点
        for key in buttons.keys():
            if buttons[key].collidepoint(pygame.mouse.get_pos()):
                buttons[key] = Label_ce(screen, label_format[key]['font_focus'], label_format[key]['text'],
                                        label_format[key]['color'], label_format[key]['position'])
            else:
                buttons[key] = Label_ce(screen, label_format[key]['font'], label_format[key]['text'],
                                        label_format[key]['color'], label_format[key]['position'])
        pygame.draw.line(screen, cfg.LINE,
                         (buttons['title'].left - 100, buttons['title'].top + buttons['title'].height - 40), (
                             buttons['title'].left + buttons['title'].width + 100,
                             buttons['title'].top + buttons['title'].height - 40))
        # 绘制Logo
        screen.blit(image, rect)
        # 事件响应
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                sys.exit(-1)
            elif event.type == pygame.MOUSEBUTTONDOWN:
                if buttons['continue'].collidepoint(pygame.mouse.get_pos()):
                    return True
                elif buttons['quit'].collidepoint(pygame.mouse.get_pos()):
                    return False
        pygame.display.update()
        clock.tick(cfg.FPS)
