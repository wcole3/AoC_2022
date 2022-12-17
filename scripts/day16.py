"""
AoC 2022 Day 16 script
"""
from collections import deque


# This is somewhat painful and I needed alot of hints from the subreddit

def parse_input(input):
    valves = {}
    tunnels = {}
    for line in input:
        valve = line.split()[1].strip()
        valves[valve] = int(line.split("=")[1].split(";")[0].strip())
        tunnels[valve] = line.split("to")[1].strip().split(" ", 1)[1].split(", ")
    return valves, tunnels


def get_distances(valves, tunnels):
    # we need to explore each valve, using brute force to find the distance between each non zero valve
    # we need to find the distance between each valve
    distances = {}
    # just doing this here for later
    nonzero_valves = [v for v in valves if valves[v] != 0]
    for valve in valves:
        # only check if flow is non zero
        if not valves[valve] and valve != 'AA':
            continue
        # we need to keep track of the nodes we have visited
        visited = {valve}
        # set initial distance value
        distances[valve] = {valve: 0}
        # we need to keep track of the nodes we need to visit
        to_visit = deque([(0, valve)])
        while to_visit:
            # remove it from the list of nodes to visit
            d, pos = to_visit.popleft()
            # add the nodes connected to the current node to the list of nodes to visit
            for node in tunnels[pos]:
                if node not in visited:
                    # add the node to the list of visited nodes
                    visited.add(node)
                    # add the node to the list of nodes to visit
                    if valves[node] != 0:
                        # we have found a node with flow, add it to the distances dict
                        distances[valve][node] = d + 1
                    to_visit.append((d + 1, node))
        # remove entries in the distance from the valve to itself
        del distances[valve][valve]
    return distances, nonzero_valves

if __name__ == '__main__':
    print("Running AoC 2022 Day 16 script")
    with open('../data/day16.txt', 'r') as f:
        data = f.read().splitlines()
        # parse each line into the values, flow rates, and tunnels
        valves, tunnels = parse_input(data)
        print(f"valves: {valves}")
        print(f"tunnels: {tunnels}")
        # now the firs trick is realizing that there are some zero flow rates in the valve list
        # we would never need to stop and open that valve, so we just treat it as a waypoint
        # now we just distance between all pairs of valves with non zero flows
        graph, nonzero_valves = get_distances(valves, tunnels)
        print(f"graph: {graph}")
        print(f"nonzero_valves: {nonzero_valves}")
        # now we need to do a search through all possible paths to find the max pressure we can release
        # Use DP cache to store the max pressure for each path and save some time; going to def in main
        cache = {}
        # also going to use a bitmask of the nonzero valves to represent if they are open or not
        indices = {v: i for i, v in enumerate(nonzero_valves) }
        # depth first search
        def dfs(time, valve, bitmask):
            if (time, valve, bitmask) in cache:
                return cache[(time, valve, bitmask)]
            maxval = 0
            for node in graph[valve]:
                # find the bit of the node
                bit = 1 << indices[node]
                if bitmask & bit:
                    # the node is already open, so we continue
                    continue
                # find the time it takes to get to the node AND open it
                travel_time = graph[valve][node] + 1
                # remaining time
                remaining_time = time - travel_time
                if remaining_time <= 0:
                    # we can't open the valve;
                    # equals to zero is here because it would release zero pressure being open for 0 sec
                    continue
                # open the valve and then continue checking, we add the amount of
                # pressure that will be release with this valve open for the remaining time
                maxval = max(maxval, dfs(remaining_time, node, bitmask | bit) + valves[node] * remaining_time)
            # add to cache
            cache[(time, valve, bitmask)] = maxval
            return maxval
        # now we just need to find the max pressure we can release
        print(f"Max pressure relieved: {dfs(30, 'AA', 0)}")
        # okay part two adds an elephant to the mix
        # we need to divide the valve problem space into two parts and see which cobination is the best
        # since bitmasks represent the open valves, we can use compliment bitmasks to "limit" the problem space explored by the pair
        # for example, if the human is given 0011 and the elephant 1100 as the starting bitmask then the human will "ignore" the first two elements
        max_pressure = 0
        for i in range(1 << len(nonzero_valves)):
            # we need to find the max pressure for each combination of human and elephant
            max_pressure = max(max_pressure, dfs(26, 'AA', i) + dfs(26, 'AA', ~i))
        print(f"Max pressure relieved with elephant: {max_pressure}")

