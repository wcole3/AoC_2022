"""
Aoc 2022 Day 11 script
"""
from math import prod

PART_TWO = True
divisor_product = 1


def destress(val):
    return val // 3


# monkey class to encode behavior
class Monkey:

    # object constructed from input string
    def __init__(self, input_str: str):
        self.items_held = None
        self.op = None
        self.test = None
        self.test_true_target = None
        self.test_false_target = None
        self.input_str = input_str
        self.parse_input()
        self.items_inspected = 0

    def parse_input(self):
        info = self.input_str.split("\n")
        self.items_held = info[0].split(":")[1].strip().split(",")
        self.op = info[1].split("=")[1].strip()
        self.test = int(info[2].split("by")[1].strip())
        self.test_true_target = int(info[3].split("monkey")[1].strip())
        self.test_false_target = int(info[4].split("monkey")[1].strip())

    def do_turn(self, monkeys: list):
        # inspect each item, modify worry, and test
        for item in self.items_held:
            self.items_inspected += 1
            # modify worry
            old = int(item)
            new = eval(self.op)
            if not PART_TWO:
                new = destress(new)
            # test item and throw to new monkey
            if new % self.test == 0:
                monkeys[self.test_true_target].items_held.append(new)
            else:
                # just highlighting that this is the trick for part two
                # We scale down the worry by the product of all the divisors
                # This can be done (i think) because all the worry operations are increasing
                # and by modulo-ing with the product divisor ensure that the worry doesn't overflow
                monkeys[self.test_false_target].items_held.append(new % divisor_product)
        self.items_held = []


if __name__ == "__main__":
    print("Aoc 2022 Day 11 script")
    with open("../data/day11.txt", "r") as f:
        input_data = f.readlines()
        monkeys = []
        for _ in range(len(input_data)):
            if "Monkey" in input_data[_]:
                _ += 1
                in_str = []
                while _ < len(input_data) and "Monkey" not in input_data[_]:
                    in_str.append(input_data[_].strip())
                    _ += 1
                _ -= 1
                monkeys.append(Monkey("\n".join(in_str)))
        # only for part we get the product of all of the test divisors
        divisor_product = prod([monkey.test for monkey in monkeys])
        print(f"divisor_product {divisor_product}")
        # run simulation
        for _ in range(10000):
            for monkey in monkeys:
                monkey.do_turn(monkeys)
            if _ % 100 == 0:
                print(f"Turn {_} complete")
        # print results
        for i, monkey in enumerate(monkeys):
            print(f"Monkey {i} inspected {monkey.items_inspected} items")
            print(f"Monkey {i} holds {monkey.items_held}")
        # calculate the product of the two highest numbers of items inspected by monkeys
        sorted_items = sorted([monkey.items_inspected for monkey in monkeys], reverse=True)
        print(f"Monkey business is {sorted_items[0] * sorted_items[1]}")
