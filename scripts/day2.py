"""
Advent of code 2022 day 2 problem
"""

# calculate the resulting score from the input rock paper scissors pairings
# Rock, Paper, Scissors
OP_REWARD = {"A": 1, "B": 2, "C": 3}
RD_REWARD = {1: 6, 0: 3, -1: 0}
RESP_MAP = {"X": "A", "Y": "B", "Z": "C"}
LOSE_TO_MAP = {"A": "B", "B": "C", "C": "A"}
WIN_TO_MAP = {"A": "C", "B": "A", "C": "B"}
REVISED_MAP = {"X": 0, "Y": 3, "Z": 6}


# is there a clever way to get the reward for a given response?
def get_round_reward(round: str):
    op_play = round.split(" ")[0]
    my_play = RESP_MAP[round.split(" ")[1]]
    reward = OP_REWARD[my_play]
    # figure out if it is a win, loss, or draw
    if op_play == my_play:
        reward += RD_REWARD[0]
    elif LOSE_TO_MAP[op_play] == my_play:
        reward += RD_REWARD[1]
    return reward

def get_revised_round_reward(round: str):
    op_play = round.split(" ")[0]
    # we know the round result
    reward = REVISED_MAP[round.split(" ")[1]]
    # figure out our play based on result
    if reward == 0:
        reward += OP_REWARD[WIN_TO_MAP[op_play]]
    elif reward == 3:
        reward += OP_REWARD[op_play]
    else:
        reward += OP_REWARD[LOSE_TO_MAP[op_play]]
    return reward

if __name__ == "__main__":
    print("Running AoC 2022 day 2")
    # get the input file
    total = 0
    rev_total = 0
    with open("../data/day2.txt", "r") as f:
        # read the file line by line
        for line in f.readlines():
            # get the reward for the round
            reward = get_round_reward(line.strip())
            rev = get_revised_round_reward(line.strip())
            total += reward
            rev_total += rev
    print(f"Total reward: {total}")
    print(f"Revised total reward: {rev_total}")
