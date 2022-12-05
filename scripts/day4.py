"""
Script for day 4 of AoC 2022
"""


def get_tuple_from_range(r: str) -> tuple:
    # parse the range
    return tuple([int(x) for x in r.split("-")])


# parse paired ranges and determine if one range in contained in the other
def is_range_contained(r1: tuple, r2: tuple) -> bool:
    # check if r1 is contained in r2
    if r1[1] >= r2[1] and r1[0] <= r2[0]:
        return True
    return False


def check_if_ranges_enclosed(line: str) -> bool:
    # parse the line
    ranges = [get_tuple_from_range(x) for x in line.strip().split(",")]
    # check if any of the ranges are contained in the other
    for i in range(len(ranges)):
        for j in range(len(ranges)):
            if i == j:
                continue
            if is_range_contained(ranges[i], ranges[j]):
                print(f"Range {ranges[j]} is contained in {ranges[i]}")
                return True
    return False


# check if the ranges intersect
def check_if_ranges_intersect(line: str) -> bool:
    # parse the line
    ranges = [get_tuple_from_range(x) for x in line.strip().split(",")]
    # check if any of the ranges are contained in the other
    for i in range(len(ranges)):
        for j in range(len(ranges)):
            if i == j:
                continue
            if ranges[i][0] <= ranges[j][1] and ranges[i][1] >= ranges[j][0]:
                print(f"Range {ranges[j]} intersects {ranges[i]}")
                return True
    return False


if __name__ == "__main__":
    print("Running AoC 2022 day 4")
    with open("../data/day4.txt", 'r') as f:
        total_enclosed = 0
        total_intersect = 0
        for line in f.readlines():
            if check_if_ranges_enclosed(line):
                total_enclosed += 1
            if check_if_ranges_intersect(line):
                total_intersect += 1
        print(f"Total enclosed: {total_enclosed}")
        print(f"Total intersect: {total_intersect}")
