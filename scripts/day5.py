"""
Day 5 AoC 2022 problem

initial config:
[V]         [T]         [J]
[Q]         [M] [P]     [Q]     [J]
[W] [B]     [N] [Q]     [C]     [T]
[M] [C]     [F] [N]     [G] [W] [G]
[B] [W] [J] [H] [L]     [R] [B] [C]
[N] [R] [R] [W] [W] [W] [D] [N] [F]
[Z] [Z] [Q] [S] [F] [P] [B] [Q] [L]
[C] [H] [F] [Z] [G] [L] [V] [Z] [H]
 1   2   3   4   5   6   7   8   9

The data file will only contain the move instructions
"""

# contruct the initial stacks from above
# the stacks are represented as a list of lists
stacks = [["C", "Z", "N", "B", "M", "W", "Q", "V"],
          ["H", "Z", "R", "W", "C", "B"],
          ["F", "Q", "R", "J"],
          ["Z", "S", "W", "H", "F", "N", "M", "T"],
          ["G", "F", "W", "L", "N", "Q", "P"],
          ["L", "P", "W"],
          ["V", "B", "D", "R", "G", "C", "Q", "J"],
          ["Z", "Q", "N", "B", "W"],
          ["H", "L", "F", "C", "G", "T", "J"]]


def get_instruction_tuple(line: str) -> tuple:
    eles = line.split(" ")
    # num, source, dest
    return eles[1], eles[3], eles[5]

def perform_iterative_move(t: tuple):
    for i in range(int(t[0])):
        source = int(t[1])
        dest = int(t[2])
        ele = stacks[source - 1].pop()
        stacks[dest - 1].append(ele)
        print(f"Moved {ele} from {source} to {dest}")
        # print(stacks)

# instead of moving iteratively, move all the elements to be moved at once
def perform_bulk_move(t: tuple):
    source = int(t[1])
    dest = int(t[2])
    eles = stacks[source - 1][-int(t[0]):]
    stacks[source - 1] = stacks[source - 1][:-int(t[0])]
    stacks[dest - 1] += eles
    print(f"Moved {eles} from {source} to {dest}")
    # print(stacks)

if __name__ == "__main__":
    print("Running AoC 2022 day 5")
    with open("../data/day5.txt", "r") as f:
        # read the file line by line
        for line in f.readlines():
            # parse the line for instructions
            instuction = get_instruction_tuple(line.strip())
            # perform_iterative_move(instuction)
            perform_bulk_move(instuction)
        # print the top element of each stack
        for i in range(len(stacks)):
            print(f"Top of stack {i + 1} is {stacks[i][-1]}")
