'''配置文件'''

SCREENSIZE = (800, 625)
HEROPICPATH = 'resources/images/hero.png'
# FONT2 = 'InkFree'
FONT = 'SegoeScript'
FONT2 = 'Consolas'
# colors
BACKGROUND = (255, 255, 255)
FOREGROUND = (0, 0, 0)
HIGHLIGHT = (255, 0, 0)
LINE = (185, 185, 185)
FPS = 30
BLOCKSIZE = 15
MAZESIZE = (15, 10)  # num_rows * num_cols
STARTPOINT = [0, 0]
DESTINATION = [14, 9]
BORDERSIZE = ((SCREENSIZE[0] - MAZESIZE[1] * BLOCKSIZE) // 2, (SCREENSIZE[1] - MAZESIZE[0] * BLOCKSIZE) // 2)
