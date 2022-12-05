"""
Scripts for the AoC 2022 event
"""


# day 1 problem: parse the input file and sum the number seperated by a new line
def find_most_cal(text: list):
    elves = {}
    max_cals = -1
    cur = 0
    elf = 0
    for line in text:
        if line != "\n":
            cur += int(line)
        else:
            # check and update
            if cur >= max_cals:
                max_cals = cur
            # store results for lulz
            elves[elf] = cur
            elf += 1
            cur = 0
    # handle last section
    if cur > 0:
        if cur >= max_cals:
            max_cals = cur
        elves[elf] = cur
    return max_cals, elves


if __name__ == "__main__":
    print("Running AoC 2022")
    # get the input file
    maxcal, elves = None, None
    with open("data/day1.txt", "r") as f:
        maxcal, elves = find_most_cal(f.readlines())
        print(f"Most calories: {maxcal}")
        print(f"Elves: {elves}")
    # part two get the top three
    top_three = sorted(elves.items(), key=lambda x: x[1], reverse=True)[:3]
    print(f"Top three: {top_three}")
    print(f"Sum of top three: {sum([x[1] for x in top_three])}")
