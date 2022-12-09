"""
AoC 2022 Day 9 script
"""


# need to simulatate a leader-follower movement on a grid
# The movment takes place on a 2d grid. The grid is infinite in all directions.
# The movement instructions direct the leader to move Up(+), Down(-), Left(-) or Right(+)
# we want to return the gird that contains information about whether the follower has visited a location

def print_grid(grid):
    # get the size from the tuples in the dict
    min_x = min(grid.keys(), key=lambda x: x[0])[0]
    max_x = max(grid.keys(), key=lambda x: x[0])[0]
    min_y = min(grid.keys(), key=lambda x: x[1])[1]
    max_y = max(grid.keys(), key=lambda x: x[1])[1]
    for y in range(max_y, min_y - 1, -1):
        for x in range(min_x, max_x + 1):
            if (x, y) in grid:
                print('#', end='')
            else:
                print('.', end='')
        print()


def move_leader(leader: tuple, instruction: str):
    if instruction[0] == 'U':
        leader = (leader[0], leader[1] + 1)
    elif instruction[0] == 'D':
        leader = (leader[0], leader[1] - 1)
    elif instruction[0] == 'L':
        leader = (leader[0] - 1, leader[1])
    elif instruction[0] == 'R':
        leader = (leader[0] + 1, leader[1])
    return leader


def move_follower(follower: tuple, leader: tuple):
    # need to check for special diagonal cases
    sqdist = (leader[0] - follower[0]) ** 2 + (leader[1] - follower[1]) ** 2
    if sqdist == 4:
        # move the follower
        if leader[0] > follower[0]:
            follower = (follower[0] + 1, follower[1])
        elif leader[0] < follower[0]:
            follower = (follower[0] - 1, follower[1])
        elif leader[1] > follower[1]:
            follower = (follower[0], follower[1] + 1)
        elif leader[1] < follower[1]:
            follower = (follower[0], follower[1] - 1)
    if sqdist > 4:
        # move diagonally
        if leader[0] > follower[0] and leader[1] > follower[1]:
            follower = (follower[0] + 1, follower[1] + 1)
        elif leader[0] > follower[0] and leader[1] < follower[1]:
            follower = (follower[0] + 1, follower[1] - 1)
        elif leader[0] < follower[0] and leader[1] > follower[1]:
            follower = (follower[0] - 1, follower[1] + 1)
        elif leader[0] < follower[0] and leader[1] < follower[1]:
            follower = (follower[0] - 1, follower[1] - 1)
    return follower


def perform_move(instructions: list, grid: dict, leader: tuple, follower: tuple):
    for instruction in instructions:
        # get the number of steps
        steps = int(instruction[1:])
        i = 0
        while i < steps:
            # move the leader
            leader = move_leader(leader, instruction)
            # move the follower if needed
            follower = move_follower(follower, leader)
            # update the grid
            grid[follower] = 1
            i += 1
            # print("----------------")
            # print_grid(grid)
    return grid


def perform_snake_move(instructions: list, grid: dict, elements: list):
    for instruction in instructions:
        steps = int(instruction[1:])
        i = 0
        while i < steps:
            # move the snake
            elements[0] = move_leader(elements[0], instruction)
            for j in range(1, len(elements)):
                elements[j] = move_follower(elements[j], elements[j - 1])
            # update the grid
            grid[elements[-1]] = 1
            i += 1
    return grid


if __name__ == '__main__':
    print("Running AoC 2022 Day 9 script")
    with open('../data/day9.txt', 'r') as f:
        data = f.readlines()
        grid = {(0, 0): 1}
        leader = (0, 0)
        follower = (0, 0)
        grid = perform_move(data, grid, leader, follower)
        # print_grid(grid)
        print(sum(grid.values()))
    # now instead of a single tail we have a chain of element, where each element is the follower of the previous one
    with open("../data/day9.txt", "r") as f:
        data = f.readlines()
        grid = {(0, 0): 1}
        followers = [(0, 0) for _ in range(10)]
        grid = perform_snake_move(data, grid, followers)
        # print_grid(grid)
        print(sum(grid.values()))
