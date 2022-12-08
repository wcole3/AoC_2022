"""
AoC 2022 day 8 script
"""


# parse the grid and find the number of trees that are visible from the edge of the grid
# A element is visible from a certain edge if it is greater than all elements between it and the edge
def find_visible_trees(grid):
    print(grid)
    # get the number of rows and columns
    num_rows = len(grid)
    num_cols = len(grid[0][0])
    print(num_rows, num_cols)
    # iterate over the grid and find the number of visible trees
    num_visible = 0
    # iterate over the columns
    for col in range(num_cols):
        # iterate over the rows
        for row in range(num_rows):
            # print(f"Testing element ({row}, {col}): {grid[row][0][col]}")
            # check the edge of the grid
            if row == 0 or row == num_rows - 1 or col == 0 or col == num_cols - 1:
                num_visible += 1
                continue
            # check if visible from any edge; don't double count
            # check if the element is visible from the bottom
            if grid[row][0][col] > max(grid[row][0][col + 1:]):
                # print("visible from bottom")
                num_visible += 1
                continue
            # check if the element is visible from the top
            if grid[row][0][col] > max(grid[row][0][:col]):
                # print("visible from top")
                num_visible += 1
                continue
            # check if the element is visible from the left
            if int(grid[row][0][col]) > max([int(row[0][col]) for row in grid[:row]]):
                # print("visible from left")
                num_visible += 1
                continue
            # check if the element is visible from the right
            if int(grid[row][0][col]) > max([int(row[0][col]) for row in grid[row + 1:]]):
                # print("visible from right")
                num_visible += 1
                continue
    return num_visible


# now find the most scenic tree by looking in each direction and determining how many trees are smaller or the same
# height
def find_most_scenic_tree(grid):
    print(grid)
    # get the number of rows and columns
    num_rows = len(grid)
    num_cols = len(grid[0][0])
    print(num_rows, num_cols)
    # iterate over the grid and find most scenic tree
    max_scenic = 0
    # iterate over the columns
    for col in range(num_cols):
        # iterate over the rows
        for row in range(num_rows):
            print(f"Testing element ({row}, {col}): {grid[row][0][col]}")
            # check the edge of the grid
            seen_right, seen_left, seen_top, seen_bottom = 0, 0, 0, 0
            if row != 0:
                # move down counting the number of trees that are smaller or the same height
                for i in range(row - 1, -1, -1):
                    if int(grid[i][0][col]) < int(grid[row][0][col]):
                        seen_top += 1
                    else:
                        seen_top += 1
                        break
            else:
                seen_top = 1
            if row != num_rows - 1:
                # move up counting the number of trees that are smaller or the same height
                for i in range(row + 1, num_rows):
                    if int(grid[i][0][col]) < int(grid[row][0][col]):
                        seen_bottom += 1
                    else:
                        seen_bottom += 1
                        break
            else:
                seen_bottom = 1
            if col != 0:
                # move left counting the number of trees that are smaller or the same height
                for i in range(col - 1, -1, -1):
                    if int(grid[row][0][i]) < int(grid[row][0][col]):
                        seen_left += 1
                    else:
                        seen_left += 1
                        break
            else:
                seen_left = 1
            if col != num_cols - 1:
                # move right counting the number of trees that are smaller or the same height
                for i in range(col + 1, num_cols):
                    if int(grid[row][0][i]) < int(grid[row][0][col]):
                        seen_right += 1
                    else:
                        seen_right += 1
                        break
            else:
                seen_right = 1
            print(f"seen right: {seen_right}, seen left: {seen_left}, seen top: {seen_top}, seen bottom: {seen_bottom}")
            # check if the senic score is the largest encountered yet
            scenic = seen_right * seen_left * seen_top * seen_bottom
            if scenic > max_scenic:
                max_scenic = scenic
    return max_scenic


if __name__ == '__main__':
    print("Running AoC 2022 day 8")
    with open("../data/day8.txt", "r") as f:
        grid = [list(map(str, line.strip().split(" "))) for line in f.readlines()]
        num_visible = find_visible_trees(grid)
        print(f"Number of visible trees: {num_visible}")
        max_scenic = find_most_scenic_tree(grid)
        print(f"Most scenic tree: {max_scenic}")
