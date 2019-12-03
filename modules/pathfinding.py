"""
Function:
    迷宫寻路算法
Arithmetic：
    A* search
    Breadth-first search
"""
from queue import Queue

'''迷宫坐标求显示位置'''


def get_pos(coordinate, block_size, border_size):
    l, t = coordinate[1] * block_size + border_size[0], coordinate[0] * block_size + border_size[1]
    coordinate = (l + block_size // 2, t + block_size // 2)
    return coordinate


'''查表 有返回下标 无返回-1'''


def check(r, c, table):
    for index, item in enumerate(table):
        if item['r'] == r and item['c'] == c:
            return index
    return -1


'''A* search'''


def A_Star(maze, starting_point, destination):
    # ----计算曼哈顿距离
    def weight(r, c, dis, er=destination[0], ec=destination[1]):
        return dis + abs(r - er) + abs(c - ec)

    # ----获取查询过的地图块
    def get_searched(block_size, border_size, table):
        searched = []
        for item in table:
            searched.append(get_pos((item['r'], item['c']), block_size, border_size))
        return searched

    path = []  # 最终路径
    open = []  # open表 能走的路
    close = []  # close表 已经走了的路
    # UP DOWN LEFT RIGHT
    directions = [(0, -1), (0, 1), (-1, 0), (1, 0)]
    block = {'parent': -1, 'r': starting_point[1], 'c': starting_point[0], 'dis': 0,
             'f': weight(starting_point[1], starting_point[0], 0)}
    # 添加起点
    open.append(block)
    while open:
        # --open根据f值表排序 取优先级最高的结点
        open = sorted(open, key=lambda x: x['f'], reverse=True)
        block = open.pop()

        # --加入close表
        close.append(block)
        # 已到达终点 根据close返回路径
        if block['r'] == destination[0] and block['c'] == destination[1]:
            next = len(close) - 1
            while next != -1:
                coordinate = (close[next]['r'], close[next]['c'])
                path.append(get_pos(coordinate, maze.block_size, maze.border_size))
                next = close[next]['parent']
            return path, get_searched(maze.block_size, maze.border_size, open + close)
        # 遍历当前结点邻近结点
        for i in range(0, 4):
            block_new = {'parent': check(block['r'], block['c'], close), 'r': block['r'] + directions[i][1],
                         'c': block['c'] + directions[i][0], 'dis': block['dis'] + 1,
                         'f': weight(block['r'] + directions[i][1], block['c'] + directions[i][0], block['dis'] + 1)}
            # 检查是否在close表中
            p = check(block_new['r'], block_new['c'], close)
            # 没有墙且不在close中
            if not maze.blocks_list[block['r']][block['c']].has_walls[i] and p == -1:
                # 检查是否在open表中
                idx = check(block_new['r'], block_new['c'], open)
                # 不在 添进open表中
                if idx == -1:
                    open.append(block_new)
                # 在 比较路径距离 短则更新
                else:
                    if open[idx]['dis'] > block_new['dis']:
                        open[idx] = block_new
    # open表为空 路径不存在
    return path, get_searched(maze.block_size, maze.border_size, open + close)


def BFS(maze, starting_point, destination):
    path = []  # 最终路径
    searched = []  # 查找过的结点
    queue = Queue(maxsize=0)  # 队列
    # UP DOWN LEFT RIGHT
    directions = [(0, -1), (0, 1), (-1, 0), (1, 0)]
    block = {'parent': None, 'r': starting_point[1], 'c': starting_point[0]}

    # ----初始化地图
    for r in range(maze.maze_size[0]):
        for c in range(maze.maze_size[1]):
            maze.blocks_list[r][c].is_visited = False

    # ----添加起点
    queue.put(block)
    searched.append(block)
    maze.blocks_list[block['r']][block['c']].is_visited = True
    while queue:
        # 出队
        block = queue.get()
        maze.blocks_list[block['r']][block['c']].is_visied = True
        # 检查是否到达终点
        if block['r'] == destination[0] and block['c'] == destination[1]:
            path.append(get_pos((block['r'], block['c']), maze.block_size, maze.border_size))
            next = block['parent']
            while not (next is None):
                path.append(get_pos((searched[next]['r'], searched[next]['c']), maze.block_size, maze.border_size))
                next = searched[next]['parent']
            for index, item in enumerate(searched):
                searched[index] = get_pos((item['r'], item['c']), maze.block_size, maze.border_size)
            return path, searched
        parent = check(block['r'], block['c'], searched)
        # 四个方向试探
        for i in range(0, 4):
            block_new = {'parent': parent, 'r': block['r'] + directions[i][1],
                         'c': block['c'] + directions[i][0]}
            # 可以走 入队
            if (not maze.blocks_list[block['r']][block['c']].has_walls[i]) and not maze.blocks_list[block_new['r']][
                block_new['c']].is_visited:
                queue.put(block_new)
                searched.append(block_new)
                maze.blocks_list[block_new['r']][block_new['c']].is_visited = True
    # 未找到路径
    for index, item in enumerate(searched):
        searched[i] = get_pos((item['r'], item['c']), maze.block_size, maze.border_size)
    return path, searched
