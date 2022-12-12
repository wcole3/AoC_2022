"""
AoC 2022 Day 12 script
"""
# alright, we're doing astar pathfinding
# start by parsing in the input and creating a grid

import numpy as np


def get_letter_priority(c: chr) -> int:
    """
    Get the priority of a letter, a-z is 1-26; A-Z is 27-52
    """
    i = ord(c)
    if i >= 97:
        return i - 96
    return i - 64 + 26
def parse_grid(lines: list):
    # I feel like I knew a clever way to do this with zip/map at one point TODO
    grid = np.ones((len(lines), len(lines[0].strip())))
    start = None
    end = None
    for x in range(len(lines)):
        for y in range(len(lines[x].strip())):
            # special cases for start and end
            if lines[x][y] == "S":
                # get start
                start = (x, y)
            elif lines[x][y] == "E":
                # get end
                end = (x, y)
                grid[x][y] = 26
            else:
                grid[x][y] = get_letter_priority(lines[x][y])
    return grid, start, end

# Apparently we're allowing large drops in elevation
def get_neighbors(pos: tuple, grid):
    # can only add neighbors that are traversable, meaning that their val = current val +/- 1
    current_pos_val = grid[pos[0]][pos[1]]
    # get the neighbors of a position
    neighbors = []
    # get the x and y
    x, y = pos
    # check the up neighbor
    if x > 0:
        if current_pos_val + 1 >= grid[x - 1][y]:
            neighbors.append((x - 1, y))
    # check the down neighbor
    if x < grid.shape[0] - 1:
        if current_pos_val + 1 >= grid[x + 1][y]:
            neighbors.append((x + 1, y))
    # check the left neighbor
    if y > 0:
        if current_pos_val + 1 >= grid[x][y - 1]:
            neighbors.append((x, y - 1))
    # check the right neighbor
    if y < grid.shape[1] - 1:
        if current_pos_val + 1 >= grid[x][y + 1]:
            neighbors.append((x, y + 1))
    return neighbors


# start with a simple distance manhattan distance
def manhattan_distance(start, end):
    return abs(start[0] - end[0]) + abs(start[1] - end[1])

# astar pathfinding
def astar(start, end, grid, h):
    # create a closed set
    closed_set = set()
    # create an open set
    open_set = set()
    # add the start to the open set
    open_set.add(start)
    # create a map of parents
    parents = {}
    # create a map of g values
    g = {}
    # set the g value of the start to 0
    g[start] = 0
    # create a map of f values
    f = {}
    # set the f value of the start to the heuristic
    f[start] = h(start, end)
    # while the open set is not empty
    while len(open_set) > 0:
        # get the current node
        current = min(open_set, key=lambda o: f[o])
        # if the current node is the end
        if current == end:
            # reconstruct the path
            path = [current]
            while current in parents:
                current = parents[current]
                path.append(current)
            path.reverse()
            return path
        # remove the current node from the open set
        open_set.remove(current)
        # add the current node to the closed set
        closed_set.add(current)
        # for each neighbor of the current node
        for neighbor in get_neighbors(current, grid):
            # if the neighbor is in the closed set
            if neighbor in closed_set:
                # skip it
                continue
            # get the tentative g score
            tentative_g = g[current] + h(neighbor, start)
            # if the neighbor is not in the open set
            if neighbor not in open_set:
                # add it to the open set
                open_set.add(neighbor)
            # if the tentative g score is worse than the current g score
            elif tentative_g >= g[neighbor]:
                # skip it
                continue
            # set the parent of the neighbor to the current node
            parents[neighbor] = current
            # set the g score of the neighbor to the tentative g score
            g[neighbor] = tentative_g
            # set the f score of the neighbor to the g score + the heuristic
            f[neighbor] = g[neighbor] + h(neighbor, end)
    # return failure
    return None

# print the path taken using < > ^ and v for the directions
def print_path_on_grid(path, grid, end):
    # set all of the grid to periods
    grid = np.full(grid.shape, ".")
    # get the first position
    x, y = path[0]
    # iterate through the path
    for i in range(1, len(path)):
        # get the next position
        nx, ny = path[i]
        # if the x is greater
        if nx > x:
            # set the grid to a v
            grid[x][y] = "v"
        # if the x is less
        elif nx < x:
            # set the grid to a ^
            grid[x][y] = "^"
        # if the y is greater
        elif ny > y:
            # set the grid to a >
            grid[x][y] = ">"
        # if the y is less
        elif ny < y:
            # set the grid to a <
            grid[x][y] = "<"
        # set the new x and y
        x, y = nx, ny
    # set the end to an E
    grid[end[0]][end[1]] = "E"
    print(grid)

if __name__ == '__main__':
    print("AoC 2022 Day 12 script")
    with open("../data/day12.txt", "r") as f:
        lines = f.readlines()
        grid, start, end = parse_grid(lines)
        print(grid)
        path = astar(start, end, grid, manhattan_distance)
        print_path_on_grid(path, grid, end)
        print(f"The length of the shortest path is {len(path) - 1}")
        # for part two we just apply this to all cells with elevation 1
        # and then find the min from those returned paths
        possible_starts = [pos for x in range(grid.shape[0]) for y in range(grid.shape[1]) for pos in [(x, y)] if grid[x][y] == 1]
        print(possible_starts)
        min_dist = np.Inf
        for start in possible_starts:
            path = astar(start, end, grid, manhattan_distance)
            if path is not None:
                min_dist = min(min_dist, len(path) - 1)
        print(f"The length of the shortest hiking trail is {min_dist}")