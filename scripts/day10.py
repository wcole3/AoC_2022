"""
AoC 2022 Day 10 script
"""

cycle_cost = {"noop" : 1, "addx" : 2}

def spin(add_last: bool, buffer: int, last: int, cycle: int):
    if add_last:
        buffer += last
        last = 0
        add_last = False
    cycle += 1
    return add_last, buffer, last, cycle

# loop over instructions and keep track of cycles and buffer
def run_program(input_data: list):
    cycles = 0
    buffer = 1
    last = 0
    add_last = False
    out = {}
    screen = ""
    for instruction in input_data:
        inst = instruction.strip().split(" ")[0]
        for _ in range(cycle_cost[inst]):
            add_last, buffer, last, cycles = spin(add_last, buffer, last, cycles)
            # print(f"cycle {cycles} buffer {buffer} last {last} add_last {add_last}")
            # update the screen
            screen_pos = (cycles - 1) % 40
            if screen_pos >= buffer - 1 and screen_pos <= buffer + 1:
                screen += "#"
            else:
                screen += "."
            # measure the buffer at certain points
            if ((cycles - 20) % 40) == 0:
                out[cycles] = buffer
        # if the last instuction was addx, setup to add x to buffer on next cycle
        if inst == "addx":
            add_last = True
            last = int(instruction.split(" ")[1])
    # spin one final time to get the final buffer value
    add_last, buffer, last, cycles = spin(add_last, buffer, last, cycles)
    # print(f"cycle {cycles} buffer {buffer} last {last} add_last {add_last}")
    return out, screen


# print the screen string to window of size 40 x 6
def print_screen(screen: str):
    for i in range(0, len(screen), 40):
        print(screen[i:i+40])


if __name__ == "__main__":
    print("Running AoC 2022 Day 10 script")
    with open("../data/day10.txt", "r") as f:
        input_data = f.readlines()
        history, screen = run_program(input_data)
        print(history)
        print(f"Sum of points {sum([key*val for key, val in history.items()])}")
        print_screen(screen)