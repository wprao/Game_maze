def A_Star(maze, starting_point, destination):
    def weight(r, c, sr=starting_point[1], sc=starting_point[0], er=destination[0], ec=destination[1]):
        return abs(r - sr) + abs(r - er) + abs(c - sc) + abs(c - ec)

    path = []
    # UP DOWN LEFT RIGHT
    directions = [(0, -1), (0, 1), (-1, 0), (1, 0)]
    block = {'r': starting_point[1], 'c': starting_point[0], 'dis': 0,
             'f': weight(starting_point[1], starting_point[0])}

    return path
