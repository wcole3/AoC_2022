"""
AoC 2022 Day 13 script
"""

import ast
from functools import cmp_to_key


# parse the input into pairs of packets; the pairs are seperated by a new line
def parse_packets(lines: list):
    # create a list of packets
    packets = []
    raw_packets = []
    # iterate through the lines
    i = 0
    while i < len(lines):
        # get the line
        line = lines[i].strip()
        # if the line is empty
        if len(line) > 0:
            # get the next line
            line2 = lines[i + 1].strip()
            # get the packet
            packet = (ast.literal_eval(line), ast.literal_eval(line2))
            # add the packet to the list
            packets.append(packet)
            raw_packets.append(ast.literal_eval(line))
            raw_packets.append(ast.literal_eval(line2))
            # increment i
            i += 2
        else:
            # increment i
            i += 1
    return packets, raw_packets


# compare a list of values; return true if for the first occurence of non equal elements, if the first element is less than the second
def compare_pure_lists(a: list, b: list):
    # special case; if lists are the same we need to keep checking; should only be called recursively
    # I feel like this is exceptionally stupid
    if a == b:
        return 0
    # iterate through the lists
    for i in range(len(a)):
        # if we run out of elements in b, return false
        if i >= len(b):
            return -1
        # check is elements are lists
        if isinstance(a[i], list) and isinstance(b[i], list):
            out = compare_pure_lists(a[i], b[i])
            if out == 0:
                continue
            else:
                return out
        elif isinstance(a[i], list):
            out = compare_pure_lists(a[i], [b[i]])
            if out == 0:
                continue
            else:
                return out
        elif isinstance(b[i], list):
            out = compare_pure_lists([a[i]], b[i])
            if out == 0:
                continue
            else:
                return out
        # if the first element is less than the second
        if a[i] < b[i]:
            return 1
        # if the first element is greater than the second
        elif a[i] > b[i]:
            return -1
    # if we get here then all the elements of a are equal to the elements of b tested thus far
    # still need to check that there aren't more elements in b
    return 1 if len(a) < len(b) else -1


# method to compare the two packets and return turn if in the right order
def compare_packet(packet):
    left = packet[0]
    right = packet[1]
    return compare_pure_lists(left, right)


if __name__ == '__main__':
    print("AoC 2022 Day 13 script")
    with open("../data/day13.txt", "r") as f:
        lines = f.readlines()
        # packets are in format [(left, right)]
        packets, raw = parse_packets(lines)
        # print(packets)
        corrects = []
        # iterate through the packets
        for i, packet in enumerate(packets):
            if compare_packet(packet) == 1:
                corrects.append(i + 1)
        print(corrects)
        print(f"Sum of correct packets indices: {sum(corrects)}")
        # part 2 seems to imply that this was a sorting problem all along
        priority = {}
        raw += [[[2]], [[6]]]
        # bless this function
        s = sorted(raw, key=cmp_to_key(compare_pure_lists), reverse=True)
        print(s)
        # get the index of [[2]] and [[6]]
        index1 = s.index([[2]]) + 1
        index2 = s.index([[6]]) + 1
        print(index1)
        print(index2)
        # print the product of the indices
        print(index2*index1)
