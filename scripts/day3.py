"""
Script to handle day 3 of AoC
"""

# parsing strings and finding the common element between them

def get_letter_priority(c: chr) -> int:
    """
    Get the priority of a letter, a-z is 1-26; A-Z is 27-52
    """
    i = ord(c)
    if i >= 97:
        return i - 96
    return i - 64 + 26

def find_common_item(s1: str, s2: str) -> str:
    # find the common item
    for c in s1:
        if c in s2:
            return c
    return None


def find_dup_item(line: str):
    # line will always be symmetric
    # get the length of the line
    length = len(line)
    # get the midpoint
    mid = length // 2
    # get the first half
    first_half = line[:mid]
    # get the second half
    second_half = line[mid:]
    return find_common_item(first_half, second_half)

def find_group_badge(lines: list) -> str:
    for c in lines[0]:
        found = True
        for line in lines[1:]:
            if c not in line:
                found = False
                break
        if found:
            return c

if __name__ == "__main__":
    print("Running AoC 2022 day 3")
    total = 0
    group_total = 0
    with open("../data/day3.txt", "r") as f:
        group = []
        for line in f.readlines():
            group.append(line.strip())
            dup = find_dup_item(line.strip())
            print(f"Duplicate: {dup}")
            total += get_letter_priority(dup)
            # test if we need to trigger group parsing
            if len(group) == 3:
                # parse the group
                gpid = find_group_badge(group)
                group = []
                group_total += get_letter_priority(gpid)
                print(f"Group badge: {gpid}")

    print(f"Total: {total}")
    print(f"Group total: {group_total}")