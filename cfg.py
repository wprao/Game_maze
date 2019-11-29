'''配置文件'''
import json

SCREENSIZE = (800, 625)
HEROPICPATH = 'resources/images/hero.png'
FONT = 'SegoeScript'
FONT2 = 'Consolas'
# colors
BACKGROUND = (255, 255, 255)
FOREGROUND = (0, 0, 0)
HIGHLIGHT = (255, 0, 0)
LINE = (185, 185, 185)
FPS = 30
BLOCKSIZE = 15
MAZESIZE = [15, 10]  # num_rows * num_cols
STARTPOINT = [0, 0]
DESTINATION = [14, 9]
BORDERSIZE = ((SCREENSIZE[0] - MAZESIZE[1] * BLOCKSIZE) // 2, (SCREENSIZE[1] - MAZESIZE[0] * BLOCKSIZE) // 2)


def write_cfg():
    cfgs = {'MAZESIZE': MAZESIZE, 'STARTPOINT': STARTPOINT, 'DESTINATION': DESTINATION}
    fp = open('cfg.txt', 'w')
    json.dump(cfgs, fp)
    fp.close()


def read_cfg():
    fp = open('cfg.txt', 'r')
    cfgs = json.load(fp)
    fp.close()
    return cfgs
