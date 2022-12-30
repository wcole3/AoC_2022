"""
AoC 2022 Day 25 script
"""

# a fun little conversion to a base 5 system with =-0123 as the digit modifiers
# some googling implies that this is a balanced quinary system
digits = {'=':-2,'-' : -1, '0' : 0, '1' : 1, '2' : 2}

def str_to_snafu(line: str):
    # reverse the line and use digits to calculate the number
    return sum(digits[c] * 5 ** i for i, c in enumerate(line[::-1]))

def decimal_to_snafu(snafu: int):
    # convert the number to a base 5 number and use digits to convert to a string
    # first convert to base five and then reverse the string
    remainder = -1
    quotient = snafu
    base_five = []
    while quotient != 0:
        quotient, remainder = divmod(quotient, 5)
        base_five.append(remainder)
    # we now have the base five number in reverse order
    # to convert to balanced quinary we loop from the least significant digit
    # and we turn 4's into '-' adding 1 to next digit and 3's into '=' adding 1 to next digit
    # we then reverse the string
    for i, e in enumerate(base_five):
        if e == 4:
            base_five[i] = '-'
            # special case for the last digit
            if i == len(base_five) - 1:
                base_five.append(1)
            else:
                base_five[i + 1] += 1
        elif e == 3:
            base_five[i] = '='
            if i == len(base_five) - 1:
                base_five.append(1)
            else:
                base_five[i+1] += 1
        elif e == 5:
            base_five[i] = '0'
            if i == len(base_five) - 1:
                base_five.append(1)
            else:
                base_five[i+1] += 1
        else:
            base_five[i] = str(e)
    return ''.join(base_five[::-1])

if __name__ == '__main__':
    print("Running AoC 2022 Day 25 script")
    with open('../data/day25.txt', 'r') as f:
        input = f.readlines()
        # convert each line to a decimal number
        numbers = []
        for line in input:
            number = str_to_snafu(line.strip())
            numbers.append(number)

        # find the sum of the numbers
        total = sum(numbers)
        print(total)
        # now convert the sum to snafu
        print(decimal_to_snafu(total))
