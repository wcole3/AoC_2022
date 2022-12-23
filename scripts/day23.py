"""
AoC 2022 Day 23 script
"""

# list of neighborhoods and the resulting move
north = ((0, 1), [(-1, 1), (0, 1), (1, 1)])
south = ((0, -1), [(-1, -1), (0, -1), (1, -1)])
east = ((1, 0), [(1, -1), (1, 0), (1, 1)])
west = ((-1, 0), [(-1, -1), (-1, 0), (-1, 1)])
global order
order = [north, south, west, east]  # this gets shuffled every round

PART_1 = False

# parse the elves and spares
def parse_board(input):
    elves = []
    for y, line in enumerate(input):
        for x, c in enumerate(line.strip()):
            if c == '#':
                elves.append((x, -y))
    return elves

# print the empty and elves together
def print_board(elves):
    # get the max and min x and y
    minx_x = min(elves, key=lambda x: x[0])[0]
    maxx_x = max(elves, key=lambda x: x[0])[0]
    miny_y = min(elves, key=lambda x: x[1])[1]
    maxy_y = max(elves, key=lambda x: x[1])[1]
    # print the board
    for y in range(maxy_y, miny_y - 1, -1):
        for x in range(minx_x, maxx_x + 1):
            if (x, y) in elves:
                print('#', end='')
            else:
                print('.', end='')
        print()

def simulate_round(elves):
    global order
    # each round consists of two phases
    # phase 1: consider moves
    # format: d[proposed move] = current pos
    proposed = {}
    duplicates = []
    needs_move = False
    for e in elves:
        # check the full neighborhood; this is inefficient but it works
        mods = []
        for o in order:
            for d in o[1]:
                neighbor = (e[0] + d[0], e[1] + d[1])
                if neighbor not in mods:
                    mods.append(neighbor)
        if not any(x in elves for x in mods):
            # no elves in the neighborhood
            continue
        needs_move = True
        # consider each possible dir we need to save the first possible move
        for d in order:
            # get the spaces to check if empty
            mods = [tuple(i+j for i,j in zip(mod, e)) for mod in d[1]]
            # if all spaces are empty, add to proposed
            if not any(m in elves for m in mods):
                new_pos = tuple(i+j for i,j in zip(d[0], e))
                # If this position was already found to be a duplicate break, this elf will not move
                if new_pos in duplicates:
                    break
                # if the new position is already in proposed, add to duplicates
                if new_pos in proposed:
                    duplicates.append(new_pos)
                    # and remove it from proposed; this elf will not move
                    del proposed[new_pos]
                    break
                proposed[new_pos] = e
                break
    # phase 2 : execute moves
    for k, v in proposed.items():
        elves.remove(v)
        elves.append(k)
    # shuffle the order before the next round; move the first element to the end
    order.append(order.pop(0))
    return elves, needs_move


def count_empty(elves):
    # find the bounds of the elves
    minx_x = min(elves, key=lambda x: x[0])[0]
    maxx_x = max(elves, key=lambda x: x[0])[0]
    miny_y = min(elves, key=lambda x: x[1])[1]
    maxy_y = max(elves, key=lambda x: x[1])[1]
    # calculate the number of space
    total_area = (maxx_x - minx_x + 1) * (maxy_y - miny_y + 1)
    return total_area - len(elves)

if __name__ == "__main__":
    print("Running AoC 2022 Day 23 script")
    with open("../data/day23.txt", "r") as f:
        elves = parse_board(f.readlines())
        # print_board(elves)
        # now we need to simulate the game
        if PART_1:
            for _ in range(10):
                elves, needs_move = simulate_round(elves)
                print(f"Round {_+1}")
                # print_board(elves)
            # find the largest rectangle containing all elves and count the emtpy spaces in it
            empty_count = count_empty(elves)
            print(f"Empty spaces: {empty_count}")
        else:
            needs_move = True
            _ = 0
            while needs_move:
                elves, needs_move = simulate_round(elves)
                _ += 1
            print(f"Rounds: {_}")
