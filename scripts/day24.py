"""
AoC 2022 Day 24 Script
"""
from collections import deque


DO_PRINT = False
# a sorta frogger like puzzle for today; (x, y) with right = +x and down = +y
dir = {">": (1, 0), "<": (-1, 0), "^": (0, -1), "v": (0, 1)}

def parse_grid(input: list):
    # parse the input to find the width and height of the grid; which are spaces that are not a wall (#)
    # aslo find the position of all blizzards indicated by the characters in dir
    width = len(input[0].strip()) - 2
    height = len(input) - 2
    grid_size = (width, height)
    blizzards = []
    for line in input[1:-1]:
        for i, c in enumerate(line[1:-1].strip()):
            if c in dir:
                # format: [x_step, y_step, x, y]
                blizzards.append([dir[c][0], dir[c][1], i, input.index(line) - 1])
    return blizzards, grid_size


def update_blizzards(blizzards, grid_size):
    # loop throught the blizzards and update their positions using the x/y steps and the grid size
    for b in blizzards:
        b[2] += b[0]
        b[3] += b[1]
        # check if the blizzard has hit a wall
        if b[2] == grid_size[0] or b[2] == -1:
            # spawn the blizzard on the other side
            b[2] = 0 if b[2] == grid_size[0] else grid_size[0] - 1
        if b[3] == grid_size[1] or b[3] == -1:
            # spawn the blizzard on the other side
            b[3] = 0 if b[3] == grid_size[1] else grid_size[1] - 1
    return blizzards

def find_next_pos(pos, blizzards, grid_size, start, end):
    # check which of the 4 neighbors and the pos itself are still valid
    neighbors = [(pos[0] + 1, pos[1]), (pos[0] - 1, pos[1]), (pos[0], pos[1] + 1), (pos[0], pos[1] - 1), pos]
    # remove anything that is out of bounds
    for n in neighbors.copy():
        if n[0] < 0 or n[0] >= grid_size[0] or n[1] < 0 or n[1] >= grid_size[1]:
            # exclude end
            if n != start and n != end:
                neighbors.remove(n)
    for b in blizzards:
        if (b[2], b[3]) in neighbors:
            neighbors.remove((b[2], b[3]))
    return neighbors

def print_grid(blizzards, grid_size):
    # print the grid with # walls around the edges and the blizzards as the characters in dir
    # the grid is 0 indexed so the top left is (-1, -1)
    for y in range(grid_size[1] + 2):
        for x in range(grid_size[0] + 2):
            if x == 0 or x == grid_size[0] + 1 or y == 0 or y == grid_size[1] + 1:
                # handle start and end
                if x == 1 and y == 0:
                    print("S", end="")
                elif x == grid_size[0] and y == grid_size[1] + 1:
                    print("E", end="")
                else:
                    print("#", end="")
            else:
                for b in blizzards:
                    if b[2] == x - 1 and b[3] == y - 1:
                        # This won't handle duplicates for now
                        print(list(dir.keys())[list(dir.values()).index((b[0], b[1]))], end="")
                        break
                else:
                    print(".", end="")
        print()
def walk(start, end, blizzards, grid_size):
    # want to get from the start to the end in the shortest amount of time
    # the blizzards move in the direction they are facing until they hit a wall; at which point they spawn on the other side
    queue = deque([[start, [start]]])
    printed_steps = []
    # need to keep track of positions we've already seen at a current step
    seen = set()
    while queue:
        # print(f"Queue size {len(queue)}")
        pos, path = queue.popleft()
        steps = len(path) - 1
        if (pos, steps) in seen:
            continue
        seen.add((pos, steps))
        # print the blizzard gird if we haven't already
        if steps not in printed_steps:
            # now need to figure out where the blizzards will be so that we know the next pos
            if DO_PRINT: print(f"Steps: {steps}")
            blizzards = update_blizzards(blizzards, grid_size)
            if DO_PRINT: print(f"Steps: {steps}")
            if DO_PRINT: print_grid(blizzards, grid_size)
            printed_steps.append(steps)
        # check if we have reached the end
        if pos == end:
            return path, blizzards
        # print_grid(blizzards, grid_size)
        # find the possible next positions from the blizzards
        possibles = find_next_pos(pos, blizzards, grid_size, start, end)
        for p in possibles:
            # could shortcut end here
            queue.append([p, path + [p]])

if __name__ == '__main__':
    print("Running AoC 2022 Day 24 Script")
    with open('../data/day24.txt', 'r') as f:
        # need to start by parsing the grid size, and the blizzard positions/directions
        # Since blizzards can occupy the same spot, I'm going to use a list of list for position
        blizzards, grid_size = parse_grid(f.readlines())
        print(f"Grid size: {grid_size}")
        if DO_PRINT: print_grid(blizzards, grid_size)
        # the start and end will always be the top left and bottom right corners
        start = (0, -1)
        end = (grid_size[0] - 1, grid_size[1])
        # now we need to find the shortest path from start to end
        path, blizzards = walk(start, end, blizzards, grid_size)
        print(f"Shortest path: {path}")
        print(f"Shortest path is {len(path) - 1} steps")
        # part two we do this search three times
        return_path, blizzards = walk(end, start, blizzards, grid_size)
        print(f"Return path: {return_path}")
        print(f"Return path is {len(return_path)} steps")
        final_path, blizzards = walk(start, end, blizzards, grid_size)
        print(f"Final path: {final_path}")
        print(f"Final path is {len(final_path)} steps")
        print(f"Total steps: {len(path) + len(return_path) + len(final_path) - 1}")