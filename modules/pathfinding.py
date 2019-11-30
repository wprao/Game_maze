def A_Star(maze, starting_point, destination):
    def weight(r,c, sr=starting_point[1], sc=starting_point[0], er=destination[0], ec=destination[1]):
        return abs(r - sr) + abs(r - er) + abs(c - sc) + abs(c - ec)

    def check(r, c, list):
        for i in range(len(list)):
            if list[i]['r'] == r and list[i]['c'] == c:
                return i
        return -1

    path = []
    open = []
    close = []
    # UP DOWN LEFT RIGHT
    directions = [(0, -1), (0, 1), (-1, 0), (1, 0)]
    block = {'parent': -1, 'r': starting_point[1], 'c': starting_point[0],
             'f': weight(starting_point[1], starting_point[0])}
    open.append(block)
    while open:
        open = sorted(open, key=lambda x: x['f'], reverse=True)
        block = open.pop()
        close.append(block)
        if block['r'] == destination[0] and block['c'] == destination[1]:
            next = len(close) - 1
            while next != -1:
                coordinate = (close[next]['r'], close[next]['c'])
                left, top = coordinate[1] * maze.block_size + maze.border_size[0], coordinate[0] * maze.block_size + \
                            maze.border_size[1]
                coordinate = (left + maze.block_size // 2, top + maze.block_size // 2)
                path.append(coordinate)
                next = close[next]['parent']
            return path
        for i in range(0, 4):
            block_new = {'parent': check(block['r'], block['c'], close), 'r': block['r'] + directions[i][1],
                         'c': block['c'] + directions[i][0],
                         'f': weight(block['r'] + directions[i][1], block['c'] + directions[i][0])}
            p = check(block_new['r'], block_new['c'], close)
            if not maze.blocks_list[block['r']][block['c']].has_walls[i] and p == -1:
                idx = check(block_new['r'], block_new['c'], open)
                if idx == -1:
                    open.append(block_new)
                else:
                    if open[idx]['f'] > block_new['f']:
                        open[idx]['parent'] = block_new['parent']
                        open[idx]['f'] = block_new['f']
    return path
