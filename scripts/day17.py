"""
AoC 2022 Day 17 script
"""
import numpy as np

# I guess we're playing tetris today
# Represent the shapes as a grid maybe
straight_row = np.array([[1, 1, 1, 1], [0, 0, 0, 0], [0, 0, 0, 0], [0, 0, 0, 0]])
cross = np.array([[0, 1, 0, 0], [1, 1, 1, 0], [0, 1, 0, 0], [0, 0, 0, 0]])
corner = np.array([[0, 0, 0, 0], [0, 0, 0, 1], [0, 0, 0, 1], [0, 1, 1, 1]])
column = np.array([[1, 0, 0, 0], [1, 0, 0, 0], [1, 0, 0, 0], [1, 0, 0, 0]])
square = np.array([[1, 1, 0, 0], [1, 1, 0, 0], [0, 0, 0, 0], [0, 0, 0, 0]])
# I just precomputing the values for left and botttom would save time
shapes = [(straight_row, 0, 0), (cross, 0, 2), (corner, 1, 3), (column, 0, 3), (square, 0, 1)]


def get_test_grid(grid, rock_shape, pos):
    grid_rows = grid[pos[0]:pos[0]+4]
    test_grid = np.zeros((4,4))
    for i in range(len(grid_rows)):
        pos_ = grid_rows[i][pos[1]:pos[1] + 4]
        if(pos_.shape[0] == 3):
            print(pos_)
        test_grid[i] = pos_ + rock_shape[i]
    return test_grid


def get_tallest_point(grid):
    for i in range(len(grid)):
        if any(grid[i][j] == 1 for j in range(len(grid[i]))):
            return i


# move the rock on the grid and check for collisions
def move_rock(grid, rock_shape, pos, input, move_step):
    # each step of movement consists of two steps, first and side to side movement
    # then a downward movement
    # maintain the move_step var as it represents where in the input we are
    # first move the rock to the left or right
    if input[move_step] == '<':
        # move the rock to the left
        pos[1] -= 1
        # try the position
        test_grid = get_test_grid(grid, rock_shape, pos)
        if any(any((test_grid[i][j] == 2 or test_grid[i][j] == 4) for j in range(len(test_grid[i]))) for i in range(len(test_grid))):
            # we hit a rock or the wall, revert movement
            pos[1] += 1
    else:
        # move right
        pos[1] += 1
        # try the position
        test_grid = get_test_grid(grid, rock_shape, pos)
        if any(any((test_grid[i][j] == 2 or test_grid[i][j] == 4) for j in range(len(test_grid[i]))) for i in range(len(test_grid))):
            # we hit a rock or the wall, revert movement
            pos[1] -= 1
    move_step = move_step + 1 if move_step % len(input) != len(input) - 1 else 0
    # test downward movement
    pos[0] += 1
    # try the position
    test_grid = get_test_grid(grid, rock_shape, pos)
    if any(any(test_grid[i][j] == 2 for j in range(len(test_grid[i]))) for i in range(len(test_grid))):
        # we hit a rock or the floor, revert movement
        pos[0] -= 1
        # add the rock to the grid
        for i in range(len(rock_shape)):
            for j in range(len(rock_shape[i])):
                if rock_shape[i][j] == 1:
                    grid[pos[0] + i][pos[1] + j] = 1
        return move_step, grid
    else:
        return move_rock(grid, rock_shape, pos, input, move_step)
def sim_rocks(input, grid, shapes, num):
    rock_num = 0
    move_step = 0
    height_deltas = []
    while rock_num < num:
        # spawn the rock on the grid
        rock_shape, left, bottom = shapes[rock_num % len(shapes)]
        # find the first highest point in the current grid
        tallest_point_on_grid = get_tallest_point(grid)
        # the first rock is a special case
        # if tallest_point_on_grid == 0:
        #     tallest_point_on_grid = len(grid) - 3
        # calculate the spawn point; this is the top left corner of the rock
        spawn_point = [(tallest_point_on_grid - 4) - bottom, 6 - left]
        # check if we need to resize the grid
        if spawn_point[0] < 0:
            new_section = np.array([[3 if (_ == 3 or _ == 11) else 0 for _ in range(15)] for _ in range(100)])
            grid = np.append(new_section, grid, axis = 0)
            spawn_point = [spawn_point[0] + 100, spawn_point[1]]
            tallest_point_on_grid = tallest_point_on_grid + 100
        # now we can add the rock to the grid
        # print(f"spawn_point: {spawn_point}")
        move_step, grid = move_rock(grid, rock_shape, spawn_point, input, move_step)
        height_deltas.append(tallest_point_on_grid - get_tallest_point(grid))
        rock_num += 1
    return grid, height_deltas


def find_pattern(heights: list[int]):
    max_pattern_length = len(heights) // 2
    for pattern_length in range(2, max_pattern_length):
        for i in range(0, len(heights) - pattern_length):
            window = heights[i : i + pattern_length]
            duplicates = 0
            next_start = i + pattern_length
            next_stop = next_start + pattern_length
            while window == heights[next_start:next_stop]:
                duplicates += 1
                if duplicates >= 5:
                    return i, window
                next_start, next_stop = (
                    next_start + pattern_length,
                    next_stop + pattern_length,
                )

if __name__ == '__main__':
    print("Running AoC 2022 Day 17 script")
    with open("../data/day17.txt", "r") as f:
        input = f.read().strip()
        # the line contains the left-right movement of the falling piece
        # the rocks alternate between left-right movement and down movement
        # the rocks are represented by a grid of 0s and 1s
        # the grid is infx9
        grid = np.array([[3 if (_ == 3 or _ == 11) else 0 for _ in range(15)] for _ in range(100)])
        # set the floor of the grid to 1s
        for i in range(13):
            grid[99][i] = 1
        # now the problems asks us to run the sim until a given number of rocks has fallen
        grid, height_history = sim_rocks(input, grid, shapes, 20000)
        # print(f"grid: {grid}")
        tallest_point_on_grid = get_tallest_point(grid)
        print(f"tallest_point_on_grid: {len(grid) - tallest_point_on_grid - 1}")
        # for part two we need to know when the pattern will repeat
        # hint: collect the change in height over time; then try to find a repeating pattern in that list
        print(f"height_history: {height_history}")
        # so if we can find the start of a repeating pattern, we can use that to calculate the final height directly
        start, window = find_pattern(height_history)
        print(f"start: {start}\twindow length: {len(window)}")
        left = sum(height_history[:start])
        middle, right = divmod(1000000000000 - start, len(window))
        middle = middle * sum(window)
        right = sum(window[:right])
        print(f"Height at insane height: {int(left + middle + right)}")


