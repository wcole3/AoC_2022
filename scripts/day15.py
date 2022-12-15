"""
AoC 2022 Day 15 Script
"""


# parse the location of the sensor and the closest beacon from the line
def parse_sensor_beacon(line: str):
    x_splits = line.strip().split("x=")
    y_splits = line.strip().split("y=")
    sensor = (int(x_splits[1].split(",")[0]), int(y_splits[1].split(":")[0]))
    beacon = (int(x_splits[2].split(",")[0]), int(y_splits[2]))
    return sensor, beacon


# calculate the manhattan distance between two points
def manhattan_distance(p1: tuple, p2: tuple):
    return abs(p1[0] - p2[0]) + abs(p1[1] - p2[1])


def count_row_coverage(pairs: dict, row: int) -> int:
    covered = 0
    # find the leftmost and rightmost beacons
    beacons_x = [val[0][0] for val in pairs.values()]
    leftmost_beacon = min(beacons_x)
    rightmost_beacon = max(beacons_x)
    # little trick here to account for x ranges that are extended by the sensor ranges
    leftmost_sensor_range = min([key[0] - val[1] for key, val in pairs.items()])
    rightmost_sensor_range = max([key[0] + val[1] for key, val in pairs.items()])
    leftmost = min(leftmost_beacon, leftmost_sensor_range)
    rightmost = max(rightmost_beacon, rightmost_sensor_range)
    print(f"leftmost: {leftmost}, rightmost: {rightmost}")
    # count the number of beacons that cover the row
    for x in range(leftmost, rightmost + 1):
        beacons = [val[0] for val in pairs.values()]
        # print(f"Testing point ({x}, {row})")
        if (x, row) not in beacons \
                and any([0 < manhattan_distance(key, (x, row)) <= val[1] \
                         for key, val in pairs.items()]):
            covered += 1
            # print("covered")
    return covered


def in_space(x, y, min_val, max_val):
    return min_val <= x <= max_val and min_val <= y <= max_val


# get a point that is 1 + radius away from a sensor
def yield_coordinates(sensor, radius, min_val, max_val):
    for d in range(radius + 1):
        # top left perimeter
        x, y = sensor[0] - radius + d - 1, sensor[1] + d
        if in_space(x, y, min_val, max_val):
            yield x, y
        # top right perimeter
        x, y = sensor[0] + radius - d + 1, sensor[1] + d
        if in_space(x, y, min_val, max_val):
            yield x, y
        # bottom left perimeter
        x, y = sensor[0] - radius + d - 1, sensor[1] - d
        if in_space(x, y, min_val, max_val):
            yield x, y
        # bottom right perimeter
        x, y = sensor[0] + radius - d + 1, sensor[1] - d
        if in_space(x, y, min_val, max_val):
            yield x, y
    yield -1, -1


def search_space(min_val, max_val, pairs):
    # first need to generate all of the points that 1 + radius away from a sensor
    points = []
    for key, val in pairs.items():
        radius = val[1]
        # get a coordinate to test
        for x, y in yield_coordinates(key, radius, min_val, max_val):
            if x == -1 and y == -1:
                break
            if all([manhattan_distance((x, y), key) > val[1] for key, val in pairs.items()]):
                return x, y


if __name__ == '__main__':
    print("AoC 2022 Day 15 script")
    # don't judge me
    PART_ONE = False
    PART_TWO = True
    with open('../data/day15.txt') as f:
        lines = f.readlines()
        # parse the sensor and beacon locations
        pairs = {}
        for line in lines:
            sensor, beacon = parse_sensor_beacon(line)
            distance = manhattan_distance(sensor, beacon)
            print(sensor, beacon, distance)
            pairs[sensor] = [beacon, distance]
        # now we want to find out how many positions are covered by a beacon in a particular row
        # we can do this by looping over every index in the row and checking if it is in the coverage of a sensor
        if PART_ONE:
            row = 10
            coverage = count_row_coverage(pairs, row)
            print(f"coverage of row {row}: {coverage}")
        # part two requires us to find the only coordinate in a reduced space that can contain a beacon
        # can loop over this set; need to reduce search space
        if PART_TWO:
            # we're told int he problem that there is only one possible location in the search space
            # this means that we only need to search the coordinates that are 1 + radius of a sensor
            # that is our reduced search space
            min_val = 0
            max_val = 4000000
            beacon_location = search_space(min_val, max_val, pairs)
            print(f"beacon location: {beacon_location}")
            print(f"Beacon frequency: {beacon_location[0] * 4000000 + beacon_location[1]}")
