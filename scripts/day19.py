"""
AoC 2022 Day 19 script
"""
import numpy as np

R = lambda *a: np.array(a)


# parse the input to determine how much each robot needs to be built
def parse_robots(input):
    blueprints = []
    for line in input:
        sentence = line.split(".")
        ore_robot_ore_cost = int(sentence[0].split("costs ")[1].split(" ")[0])
        clay_robot_ore_cost = int(sentence[1].split("costs ")[1].split(" ")[0])
        obsidian_robot_ore_cost = int(sentence[2].split("costs ")[1].split(" ")[0])
        obsidian_robot_clay_cost = int(sentence[2].split("costs ")[1].split(" ")[3])
        geode_robot_ore_cost = int(sentence[3].split("costs ")[1].split(" ")[0])
        geode_robot_obsidian_cost = int(sentence[3].split("costs ")[1].split(" ")[3])
        # format robots in a common format in terms of what it produces and what it costs
        ore_robot = [R(0, 0, 0, 1), R(0, 0, 0, ore_robot_ore_cost)]
        clay_robot = [R(0, 0, 1, 0), R(0, 0, 0, clay_robot_ore_cost)]
        obsidian_robot = [R(0, 1, 0, 0), R(0, 0, obsidian_robot_clay_cost, obsidian_robot_ore_cost)]
        geode_robot = [R(1, 0, 0, 0), R(0, geode_robot_obsidian_cost, 0, geode_robot_ore_cost)]
        blueprints.append([ore_robot, clay_robot, obsidian_robot, geode_robot])
    return blueprints


key = lambda a: tuple(a[0] + a[1]) + tuple(a[1])
prune = lambda x: sorted({key(x): x for x in x}.values(), key=key)[-10000:]

def run_blueprint(blueprint, time):
    # that starting state is the same for all blueprints
    # format: stockpile, robots
    state = [(R(0, 0, 0, 0), R(0, 0, 0, 1))]
    # now check every possible choice at each minute until we run out of time
    for t in range(time, 0, -1):
        # check all possible choices
        new_state = []
        for stockpile, robots in state:
            # check if we can build a robot
            for robot in blueprint:
                # check if we have enough resources to build the robot
                if np.all(stockpile >= robot[1]):
                    # we can build this robot type; account for production in update
                    new_state.append((stockpile - robot[1] + robots, robots + robot[0]))
                else:
                    # saw a very clever trick to use a robot with all zeros to account for this condition in the loop above
                    # we cannot build this robot type; account for production in update
                    new_state.append((stockpile + robots, robots))
        # update the state; we have to prune this somehow; try a simple heuristic
        # tried heuristics:
        # only keeping that 1000 with the largest stockpile -> failed 0 geodes
        # only keeping that 1000 with the largest stockpile and largest robots -> failed 0 geodes
        # just sort on the stockpile -> failed 0 geodes
        # try weighting the stockpile by the number of robots -> failed 0 geodes
        # I guess I'm a fucking imbecile and can figure out how to sort this properly so I just took a prune function that worked from online
        # I'm more frustrated by this than I should be
        state = prune(new_state)
        print(f"Time {t}: {len(state)} possible states")
    # return the max value of geodes
    return max([stockpile[0] for stockpile, robots in state])


if __name__ == "__main__":
    print("Running AoC 2022 Day 19 script")
    with open("../data/day19.txt") as f:
        lines = f.readlines()
        blueprints = parse_robots(lines)
        # print(blueprints)
        # I guess Im going to set up a dfs to explore every possible path in the tree
        # we start with 24 minutes and 1 ore collecting robot
        # every minute we can make a decision to build a new robot or not; this should be the goal of a branch
        # we can build a robot if we have enough resources
        # we'll need to prune some branchs and need to know stop conditions
        # for example if based on the time remaining we can't build another geode robot, we can prune that branch
        geodes = []
        for i, blueprint in enumerate(blueprints):
            geodes_num = run_blueprint(blueprint, 24)
            geodes.append((geodes_num, geodes_num * (i+1)))
        print(geodes)
        print(sum([x[1] for x in geodes]))
        # part 2
        geodes = []
        for blueprint in blueprints[:3]:
            geodes_num = run_blueprint(blueprint, 32)
            geodes.append(geodes_num)
        print(geodes)
        print(np.prod(geodes))
