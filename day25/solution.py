import itertools

from intcode.intcode import read_program, VM

input_strings = ["north\n",
                 "take mug\n",
                 "north\n",
                 "take food ration\n",
                 "south\n",
                 "east\n",
                 "north\n",
                 "east\n",
                 "take semiconductor\n",
                 "west\n",
                 "south\n",
                 "west\n",
                 "south\n",
                 "east\n",
                 "take ornament\n",
                 "north\n",
                 "take coin\n"
                 "east\n",
                 "take mutex\n",
                 "west\n",
                 "south\n",
                 "east\n",
                 "take candy cane\n",
                 "west\n",
                 "west\n",
                 "south\n",
                 "east\n",
                 "take mouse\n",
                 "south\n"]

items = ["food ration",
         "candy cane",
         "mouse",
         "mug",
         "ornament",
         "semiconductor",
         "mutex",
         "coin"]

input_string = "".join(input_strings)

def input_generator(items_to_carry):
    for a in input_string:
        yield ord(a)

    for item in items:
        for c in "drop " + item + "\n":
            yield ord(c)

    for item in items_to_carry:
        for c in "take " + item + "\n":
            yield ord(c)

    for c in "inv\nwest\n":
        yield ord(c)

    while True:
        for c in input("Next instruction: "):
            yield ord(c)
        yield ord("\n")


def try_combination(items_to_carry):
    program = read_program("input.txt")
    vm = VM(program)

    generator = input_generator(items_to_carry)
    vm.get_input_callback = lambda: next(generator)

    current_string = ""
    is_it = True
    while True:
        try:
            current_c = vm.get_ascii_output()
            current_string += current_c
            if current_c == "\n":
                if "A loud, robotic voice says" in current_string:
                    if "lighter" in current_string or "heavier" in current_string:
                        is_it = False
                    break
                current_string = ""
        except StopIteration:
            break

    if is_it:
        print("Required items:", items_to_carry)

for combination_size in range(1, len(items) + 1):
    combinations = list(itertools.combinations(items, combination_size))
    for combination in combinations:
        try_combination(combination)

