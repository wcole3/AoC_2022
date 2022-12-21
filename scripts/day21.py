"""
AoC 2022 Day 21 Script
"""

import re

global op_monkeys, num_monkeys


PART_1 = False
def parse_monkeys(input: list):
    global op_monkeys, num_monkeys
    op_monkeys = {}
    num_monkeys = {}
    for line in input:
        id_and_op = line.strip().split(":")
        id = id_and_op[0]
        if any(x in id_and_op[1] for x in ["+", "*", "/", "-"]):
            children = re.split('(\+|\*|\/|-)', id_and_op[1])
            op_monkeys[id] = (children[0].strip(), children[2].strip(), children[1].strip())
        else:
            num_monkeys[id] = int(id_and_op[1].strip())
    return op_monkeys, num_monkeys


def eval_monkey(id: str):
    global op_monkeys, num_monkeys
    if id in num_monkeys:
        return num_monkeys[id]
    else:
        mon1 = eval_monkey(op_monkeys[id][0])
        if mon1 not in num_monkeys:
            num_monkeys[op_monkeys[id][0]] = mon1
        mon2 = eval_monkey(op_monkeys[id][1])
        if mon2 not in num_monkeys:
            num_monkeys[op_monkeys[id][1]] = mon2
        # evaluate the operation
        result = eval(f"{mon1} {op_monkeys[id][2]} {mon2}")
        num_monkeys[id] = result
        return result

def get_comp_operation(op: str):
    if op == "+":
        return "-"
    elif op == "-":
        return "+"
    elif op == "*":
        return "/"
    elif op == "/":
        return "*"

# part 2 algorithm
def get_human_number(id: str, target: int):
    global op_monkeys, num_monkeys
    if "humn" == id:
        return target
    # we start by figuring out which of the children depend on humn
    child1 = op_monkeys[id][0]
    child2 = op_monkeys[id][1]
    # the compliment operation depends on the order too
    operation = get_comp_operation(op_monkeys[id][2])
    try:
        child1_result = eval_monkey(child1)
        # print(f"Child 2 {child2} depends on humn")
        # print(f"child1_result: {child1_result}")
        # the target is what we're trying to achieve eventually
        # order matters here
        new_target = 0
        if operation == "+":
            new_target = child1_result - target
        elif operation == "*":
            new_target = child1_result / target
        else:
            new_target = eval(f"{target} {operation} {child1_result}")
        return get_human_number(child2, new_target)
    except:
        # print(f"Child 1 {child1} depends on humn")
        child2_result = eval_monkey(child2)
        # print(f"child2_result: {child2_result}")
        # order doesn't matter here
        new_target = eval(f"{target} {operation} {child2_result}")
        return get_human_number(child1, new_target)

if __name__ == '__main__':
    global op_monkeys, num_monkeys
    print("Running AoC 2022 Day 21 Script")
    with open("../data/day21.txt", "r") as f:
        data = f.readlines()
        # so the we need to figure out what the root monkey is going to say which requires
        # finding out what alot of other monkeys say
        # Im going to start with two dicts, one for a known monkey number; and one for operation monkeys
        # After parsing I'll loop through the operation monkeys and recursivly evaluate numbers
        op_monkeys, num_monkeys = parse_monkeys(data)
        print(f"Operation monkeys: {op_monkeys}")
        print(f"Number monkeys: {num_monkeys}")
        # now start with the root monkey and work down
        if PART_1:
            result = eval_monkey("root")
            print(f"Result: {result}")
        else:
            # part 2
            # okay so the rules change
            # the root monkey is a equality operation
            # the humn monkey is YOU, and you need to figure out what number humn should say so that root monkey says 0
            # maybe we can figure out which of roots child monkeys depends on humn
            # then we could recurse go down that chain
            # first clear humn entry whereever it is
            if "humn" in num_monkeys:
                num_monkeys["humn"] = '?'
            # figure out which of the children of root depends on humn
            child1 = op_monkeys["root"][0]
            child2 = op_monkeys["root"][1]
            try:
                child1_result = eval_monkey(child1)
                print(f"Child 2 {child2} depends on humn")
                print(f"child1_result: {child1_result}")
                result = get_human_number(child2, child1_result)
                print(f"Result: {result}")
            except:
                print(f"Child 1 {child1} depends on humn")
                child2_result = eval_monkey(child2)
                print(f"child2_result: {child2_result}")
                result = get_human_number(child1, child2_result)
                print(f"Result: {result}")


