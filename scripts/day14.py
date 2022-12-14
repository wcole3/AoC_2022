"""
AoC 2022 Day 14 script
"""


# just a fun print method
def print_grid(grid: list):
    for row in grid:
        print("".join(row))


def print_sand(sand, rocks):
    # limits of the grid
    xs = [x for x, y in rocks]
    ys = [y for x, y in rocks]
    min_x = min(xs)
    max_x = max(xs)
    min_y = min(ys)
    max_y = max(ys)
    # create the grid
    grid = []
    for y in range(min_y, max_y + 1):
        row = []
        for x in range(min_x, max_x + 1):
            if (x, y) == (0, 0):
                row.append("+")
            elif (x, y) in rocks:
                row.append("#")
            elif (x, y) in sand:
                row.append("0")
            else:
                row.append(".")
        grid.append(row)
    print_grid(grid)


def print_rock_grid(rocks):
    print_sand(set(), rocks)


# parses the grid
def parse_grid(lines: list):
    # The starting location is defined at 500, 0 so we will reindex that to 0,0
    # down is the positive y direction and right is the positive x direction
    offset = 500
    rocks = set()
    rocks.add((0, 0))
    for line in lines:
        line = line.strip().split(" -> ")
        for i in range(1, len(line)):
            # get the coordinates of the ends of the line segment
            x1, y1 = line[i - 1].strip().split(",")
            x2, y2 = line[i].strip().split(",")
            # now add rock entries for each point in the line segment
            # if the line is vertical; pretty sure this is always top down but we can check
            if x1 == x2:
                start = int(y1) if int(y1) < int(y2) else int(y2)
                end = int(y2) if int(y1) < int(y2) else int(y1)
                # iterate through the y values
                for y in range(start, end + 1):
                    # add the rock
                    rocks.add((int(x1) - offset, y))
            # if the line is horizontal; careful can go either way
            elif y1 == y2:
                # iterate through the x values
                start = int(x1) if int(x1) < int(x2) else int(x2)
                end = int(x2) if int(x1) < int(x2) else int(x1)
                for x in range(start, end + 1):
                    # add the rock
                    rocks.add((x - offset, int(y1)))
    # now get the max and min for x and y and create the grid
    xs = [x for x, y in rocks]
    ys = [y for x, y in rocks]
    min_x = min(xs)
    max_x = max(xs)
    min_y = min(ys)
    max_y = max(ys)

    return rocks, min_x, max_x, min_y, max_y


def move_sand(rocks: set, sand: set, pos: tuple, max_y: int, max_x: int, min_x: int, with_floor: bool = False):
    # test the pos against the rule
    if not with_floor:
        if pos[1] + 1 > max_y or pos[0] < min_x or pos[0] > max_x:
            # sand will fall off the grid
            return None, rocks
    # try moving the sand down
    if (pos[0], pos[1] + 1) not in rocks and (pos[0], pos[1] + 1) not in sand:
        # move the sand down
        new_pos = (pos[0], pos[1] + 1)
        return move_sand(rocks, sand, new_pos, max_y, max_x, min_x, with_floor=with_floor)
    # try moving the sand down and left
    elif (pos[0] - 1, pos[1] + 1) not in rocks and (pos[0] - 1, pos[1] + 1) not in sand:
        # move the sand down and left
        new_pos = (pos[0] - 1, pos[1] + 1)
        if with_floor and new_pos[0] < min_x:
            # add more floor in that direction
            rocks.add((new_pos[0], max_y))
            min_x = new_pos[0]
            # resim
            return move_sand(rocks, sand, pos, max_y, max_x, min_x, with_floor=with_floor)
        else:
            return move_sand(rocks, sand, new_pos, max_y, max_x, min_x, with_floor=with_floor)
    # try moving the sand down and right
    elif (pos[0] + 1, pos[1] + 1) not in rocks and (pos[0] + 1, pos[1] + 1) not in sand:
        # move the sand down and right
        new_pos = (pos[0] + 1, pos[1] + 1)
        if with_floor and new_pos[0] > max_x:
            # add more floor in that direction
            rocks.add((new_pos[0], max_y))
            max_x = new_pos[0]
            # resim
            return move_sand(rocks, sand, pos, max_y, max_x, min_x, with_floor=with_floor)
        return move_sand(rocks, sand, new_pos, max_y, max_x, min_x, with_floor=with_floor)
    # if none of these are true, then the sand is stuck
    return pos, rocks


def run_sim(rocks, with_floor: bool = False):
    # limits of the grid
    xs = [x for x, y in rocks]
    ys = [y for x, y in rocks]
    min_x = min(xs)
    max_x = max(xs)
    min_y = min(ys)
    max_y = max(ys)
    # we keep simming sand until we get a stable state
    # The stable state is reached once a grain of sand falls off the grid; NOT when it cant move
    sand_on_grid = 0
    sand = set()
    while True:
        start = (0, 0)
        # move the sand
        new_pos, rocks = move_sand(rocks, sand, start, max_y, max_x, min_x, with_floor=with_floor)
        if new_pos is None:
            # the sand fell off the grid
            break
        # add the sand to the set
        sand.add(new_pos)
        sand_on_grid += 1
        if new_pos == start:
            # the sand has reached the top
            break
    return sand_on_grid, sand, rocks


if __name__ == '__main__':
    print("AoC 2022 Day 14 script")
    with open("../data/day14.txt", "r") as f:
        lines = f.readlines()
        # first we need to parse the input such that we get the grid of rock tiles
        rocks, min_x, max_x, min_y, max_y = parse_grid(lines)
        print_rock_grid(rocks)
        # now need to sim the sand falling
        sand_count, sand, _ = run_sim(rocks)
        print(f"Sand count: {sand_count}")
        print_sand(sand, rocks)
        # for part two we add on infinite floor
        # we can do this by adding a row of rocks at the bottom
        # in the sim we will handle dynamically adding more floor
        # of course could just add more rocks here and empirically find enough floor, but this will be more fun
        for x in range(min_x, max_x + 1):
            rocks.add((x, max_y + 2))
        # now we can run the sim again
        floor_sand_count, sand, rocks = run_sim(rocks, with_floor=True)
        print_sand(sand, rocks)
        print(f"Sand count with floor: {floor_sand_count}")
