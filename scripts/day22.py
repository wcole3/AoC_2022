"""
AoC 2022 Day 22 Script
"""

# So todays problem is navigating through a map from a set of instructions with wraparound
# THat seems straightforward, but I'm trying to think about what the complication in part 2 could be

import numpy as np

# rotation is clockwise, ie R 0 -> 1 -> 2 -> 3 -> 0; L 0 -> 3 -> 2 -> 1 -> 0
dirs = {"^": 3, ">": 0, "v": 1, "<": 2}
global grid, left, right, top, bottom, faces, extents

PART_1 = False


def parse_instruction(inst):
    instructions = []
    # parse the instruction
    # go through character wise and group numbers together and break on letters
    i = 0
    number = ""
    while i < len(inst):
        if inst[i].isnumeric():
            number += inst[i]
        else:
            instructions.append(int(number))
            number = ""
            instructions.append(inst[i])
        i += 1
    # make sure we get the last instuction
    if number:
        instructions.append(int(number))
    return instructions


def parse_grid(input):
    # find the max row size
    max_row = max([len(row) for row in input])
    grid = np.zeros((len(input), max_row))
    print(f"Grid size: {grid.shape}")
    for j, line in enumerate(input):
        # go character wise and set value to 1 if open(.), and 2 if wall(#)
        for i, char in enumerate(line):
            if char == ".":
                grid[j][i] = 1
            elif char == "#":
                grid[j][i] = 2
    # I think it will be useful later to know the left void and right void for each row and top/bottom voids for columns
    # so we can wrap around
    left_extent = []
    right_extent = []
    top_extend = []
    bottom_extend = []
    for i in range(grid.shape[0]):
        filled_grid = np.where(grid[i] > 0)
        left_extent.append(filled_grid[0][0])
        right_extent.append(filled_grid[0][-1])
    for i in range(grid.shape[1]):
        filled_grid = np.where(grid[:, i] > 0)
        top_extend.append(filled_grid[0][0])
        bottom_extend.append(filled_grid[0][-1])
    return grid, left_extent, right_extent, top_extend, bottom_extend


def parse_input(input):
    # the last line will be the instructions, and the rest is the grid
    inst = input[-1]
    grid = input[:-2]  # skip break line and instructions
    # parse each
    instructions = parse_instruction(inst)
    grid_array, left, right, top, bottom = parse_grid(grid)
    return grid_array, left, right, top, bottom, instructions


def get_faces_from_grid(grid):
    long_side = max(grid.shape)
    face_len = int(long_side / 4)
    # split the grid into all segments
    faces = []
    extents = []
    for i in range(0, grid.shape[0], face_len):
        for j in range(0, grid.shape[1], face_len):
            if np.sum(grid[i:i + face_len, j:j + face_len]) > 0:
                faces.append(grid[i:i + face_len - 1, j:j + face_len - 1])
                extents.append((j, j + face_len - 1, i, i + face_len - 1))
    return faces, extents

def get_face_index(face):
    global faces
    for i, t in enumerate(faces):
        if t[0] == face:
            return i

def get_new_face_pos(pos, dir, current_face, old_face, old_dir, old_pos, rot):
    global grid, left, right, top, bottom, faces, extents
    left_extent = left[old_pos[0]]
    right_extent = right[old_pos[0]]
    top_extent = top[old_pos[1]]
    bottom_extent = bottom[old_pos[1]]
    # calculate the offset between the old face and the new face of the top left corner
    curr_face_index = get_face_index(current_face)
    curr_face_extents = extents[curr_face_index]
    old_face_index = get_face_index(old_face)
    old_face_extents = extents[old_face_index]
    # calculate the offset
    offset = (old_face_extents[0] - curr_face_extents[0], old_face_extents[2] - curr_face_extents[2])
    # calculate where the old point was in the old face relative to the top corner
    x_delta = old_pos[1] - old_face_extents[0]
    y_delta = old_pos[0] - old_face_extents[2]
    if rot == 0:
        # if there's no rotation
        if old_dir == 0:
            # going right
            pos[0] = curr_face_extents[2] + y_delta
            pos[1] = curr_face_extents[0]
        elif old_dir == 1:
            # going down
            pos[0] = curr_face_extents[2]
            pos[1] = curr_face_extents[0] + x_delta
        elif old_dir == 2:
            # going left
            pos[0] = curr_face_extents[2] + y_delta
            pos[1] = curr_face_extents[1]
        elif old_dir == 3:
            # going up
            pos[0] = curr_face_extents[3]
            pos[1] = curr_face_extents[0] + x_delta
    elif rot == 1:
        # we are rotating clockwise, so top -> left, left -> bottom, bottom -> right, right -> top
        if old_dir == 0:
            # if we were facing right, we are now facing down
            pos[0] = curr_face_extents[2]
            pos[1] = curr_face_extents[1] - y_delta
        elif old_dir == 1:
            # if we were facing down, we are now facing left
            pos[0] = curr_face_extents[2] + x_delta
            pos[1] = curr_face_extents[1]
        elif old_dir == 2:
            # if we were facing left, we are now facing up
            pos[0] = curr_face_extents[3]
            pos[1] = curr_face_extents[1] - y_delta
        elif old_dir == 3:
            # if we were facing up, we are now facing right
            pos[0] = curr_face_extents[2] + x_delta
            pos[1] = curr_face_extents[0]
    elif rot == -2:
        #rotation 180 degrees so top -> top, bottom -> bottom, left -> left, right -> right
        if old_dir == 0:
            # went from right to right
            pos[0] = curr_face_extents[3] - y_delta
            pos[1] = curr_face_extents[1]
        elif old_dir == 1:
            # went from bottom to bottom
            pos[0] = curr_face_extents[3]
            pos[1] = curr_face_extents[1] - x_delta
        elif old_dir == 2:
            # went from left to left
            pos[0] = curr_face_extents[3] - y_delta
            pos[1] = curr_face_extents[0]
        elif old_dir == 3:
            # went from top to top
            pos[0] = curr_face_extents[2]
            pos[1] = curr_face_extents[1] - x_delta
    elif rot == -1:
        # rotation counter clockwise, so top -> right, right -> bottom, bottom -> left, left -> top
        if old_dir == 0:
            # went from right to up
            pos[0] = curr_face_extents[3]
            pos[1] = curr_face_extents[0] + y_delta
        elif old_dir == 1:
            # went from down to right
            pos[0] = curr_face_extents[2] - x_delta
            pos[1] = curr_face_extents[0]
        elif old_dir == 2:
            # went from left to down
            pos[0] = curr_face_extents[2]
            pos[1] = curr_face_extents[0] + y_delta
        elif old_dir == 3:
            # went from up to left
            pos[0] = curr_face_extents[3] - x_delta
            pos[1] = curr_face_extents[1]
    else:
        print(f"Something went wrong unhandled rotation: {rot}")
    if pos[0] < 0 or pos[0] >= grid.shape[0] or pos[1] < 0 or pos[1] >= grid.shape[1]:
        print(f"Something went wrong, new position is out of bounds: {pos}")
    return pos


def move(pos, dir, step, current_face='A', mapping = None):
    global grid, left, right, top, bottom, faces, extents
    # dir cases
    if step == 'L' or step == 'R':
        if step == 'L':
            dir = (dir - 1) % 4
        else:
            dir = (dir + 1) % 4
        return pos, dir, current_face
    else:
        # get the left and right extent of the row
        left_extent = left[pos[0]]
        right_extent = right[pos[0]]
        top_extent = top[pos[1]]
        bottom_extent = bottom[pos[1]]
        for _ in range(step):
            mod = 0
            index = -1
            if dir == 0 or dir == 2:
                mod = 1 if dir == 0 else -1
                index = 1
            else:
                mod = 1 if dir == 1 else -1
                index = 0
            # could do this with a while loop, but that might be slow, try it
            old_pos = pos.copy()
            old_dir = dir
            old_face = current_face
            if not PART_1:
                current_face_index = get_face_index(current_face)
            pos[index] += mod
            # if we are out of bounds, wrap around
            if index == 1:
                if PART_1:
                    if pos[1] < left_extent:
                        pos[1] = right_extent
                    elif pos[1] > right_extent:
                        pos[1] = left_extent
                else:
                    if pos[1] < extents[current_face_index][0]:
                        # moved off left of face
                        rot = mapping[current_face_index][0][0]
                        dir += rot
                        dir = dir % 4
                        current_face = mapping[current_face_index][0][1]
                        # get the new position based off the rotation and new face
                        pos = get_new_face_pos(pos, dir, current_face, old_face, old_dir, old_pos, rot)
                    elif pos[1] > extents[current_face_index][1]:
                        # moved off right
                        rot = mapping[current_face_index][1][0]
                        dir += rot
                        dir = dir % 4
                        current_face = mapping[current_face_index][1][1]
                        pos = get_new_face_pos(pos, dir, current_face, old_face, old_dir, old_pos, rot)
            else:
                if PART_1:
                    if pos[0] < top_extent:
                        pos[0] = bottom_extent
                    elif pos[0] > bottom_extent:
                        pos[0] = top_extent
                else:
                    if pos[0] < extents[current_face_index][2]:
                        # moved off top of face
                        rot = mapping[current_face_index][2][0]
                        dir += rot
                        dir = dir % 4
                        current_face = mapping[current_face_index][2][1]
                        pos = get_new_face_pos(pos, dir, current_face, old_face, old_dir, old_pos, rot)
                    elif pos[0] > extents[current_face_index][3]:
                        # moved off bottom
                        rot = mapping[current_face_index][3][0]
                        dir += rot
                        dir = dir % 4
                        current_face = mapping[current_face_index][3][1]
                        pos = get_new_face_pos(pos, dir, current_face, old_face, old_dir, old_pos, rot)

            # stop if we hit a wall
            if grid[pos[0]][pos[1]] == 2:
                pos = old_pos
                dir = old_dir
                current_face = old_face
                break

        return pos, dir, current_face

def print_grid(pos, dir):
    global grid
    for i in range(len(grid)):
        for j in range(len(grid[i])):
            if i == pos[0] and j == pos[1]:
                if dir == 0:
                    print('>', end='')
                elif dir == 1:
                    print('v', end='')
                elif dir == 2:
                    print('<', end='')
                elif dir == 3:
                    print('^', end='')
            else:
                if grid[i][j] == 0:
                    print(' ', end='')
                elif grid[i][j] == 1:
                    print('.', end='')
                elif grid[i][j] == 2:
                    print('#', end='')
        print()

if __name__ == '__main__':
    global grid, left, right, top, bottom, faces, extents
    print("Running AoC 2022 Day 22 Script")
    with open("../data/day22.txt", "r") as f:
        data = f.read().splitlines()
        # parse the grid and the instructions
        grid, left, right, top, bottom, instructions = parse_input(data)
        # now we need to navigate through the grid
        # doing each step one at a time is probably too inefficent for whatever part 2 is
        # maybe we can update a move step via calculation
        # first get the starting position which is the first 1 in the top row
        pos = [0, np.where(grid[0] == 1)[0][0]]
        print(f"Starting position: {pos}")
        dir = dirs[">"]
        if PART_1:
            for step in instructions:
                pos, dir, face = move(pos, dir, step)
                # print(f"New position: {pos}, New direction: {dir}")
            # calculate the final pass word
            password = (1000 * (pos[0] + 1)) + ((pos[1] + 1) * 4) + dir
            print(f"Final password: {password}")
        # OMG its a cube part 2
        # my first thought is to see if we can construct a surrogate 2d grid from the cube faces using duplicate faces
        # that would allow us to not change the code much
        # Obs: there are only 3 straight paths around a cubes faces that you can take
        # Im a little stuck so I'm just going to do something by parsing the grid into 6 face arrays
        faces, extents = get_faces_from_grid(grid)
        # zip a label to the faces
        faces = list(zip(['A', 'B', 'C', 'D', 'E', 'F'], faces))

        # now we need to get the mapping from one face's side to another this would work
        # by checking if a move step takes the pos outside the extents of the current face if it does, figure out the
        # new face, and the rotation of dir to get to the new face Im not sure how to figure this out except by
        # manually inputting it; there has to be a folding algorithm
        # Format: ((off left rotation, new face),
        # (off right rotation, new face),
        # (off top rotation, new face),
        # (off bottom rotation, new face))
        test_face_mapping = (
            ((-1, 'C'), (-2, 'F'), (-2, 'B'), (0, 'D')),  # A mapping
            ((1, 'F'), (0, 'C'), (-2, 'A'), (-2, 'E')),  # B mapping
            ((0, 'B'), (0, 'D'), (1, 'A'), (-1, 'E')),  # C mapping
            ((0, 'C'), (1, 'F'), (0, 'A'), (0, 'E')),  # D mapping
            ((1, 'C'), (0, 'F'), (0, 'D'), (-2, 'B')),  # E mapping
            ((0, 'E'), (-2, 'A'), (-1, 'D'), (-1, 'B'))  # F mapping
        )
        problem_face_mapping = (
            ((-2, 'D'), (0, 'B'), (1, 'F'), (0, 'C')),  # A mapping
            ((0, 'A'), (-2, 'E'), (0, 'F'), (1, 'C')),  # B mapping
            ((-1, 'D'), (-1, 'B'), (0, 'A'), (0, 'E')),  # C mapping
            ((-2, 'A'), (0, 'E'), (1, 'C'), (0, 'F')),  # D mapping
            ((0, 'D'), (-2, 'B'), (0, 'C'), (1, 'F')),  # E mapping
            ((-1, 'A'), (-1, 'E'), (0, 'D'), (0, 'B'))  # F mapping
        )
        # after writing that out I wonder if it could have been a matrix
        if not PART_1:
            face = 'A'

            for step in instructions:
                pos, dir, face = move(pos, dir, step, face, problem_face_mapping)
                # print(f"Grid after step: {step}")
                # print_grid(pos, dir)
            # calculate the final pass word
            password = (1000 * (pos[0] + 1)) + ((pos[1] + 1) * 4) + dir
            print(f"Final password: {password}")
