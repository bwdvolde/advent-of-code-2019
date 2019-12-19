from intcode.intcode import read_program, VM
import numpy as np

LEFT = "LEFT"
RIGHT = "RIGHT"
UP = "UP"
DOWN = "DOWN"


def get_dr_dc(direction):
    return {
        LEFT: (0, -1),
        RIGHT: (0, 1),
        UP: (-1, 0),
        DOWN: (1, 0)
    }[direction]


program = read_program("input.txt")
vm = VM(program)


def read_world(vm):
    string = ""
    while True:
        try:
            string += chr(vm.get_output())
        except StopIteration:
            break
    return string


string = read_world(vm)
world = [[c for c in line] for line in string.rstrip("\n").split("\n")]


def print_world(world):
    for r, row in enumerate(world):
        for c, char in enumerate(row):
            print(char, end="")
        print()


def find_min_row_col(world):
    min_row = 99999999
    min_col = 99999999
    for r, row in enumerate(world):
        for c, char in enumerate(row):
            if char == "#":
                min_row = min(min_row, r)
                min_col = min(min_col, c)
    return min_row, min_col


def calculate_alignment_sum(world, min_row, min_col):
    alignment_sum = 0
    for r, row in enumerate(world):
        for c, char in enumerate(row):
            if 0 < r < len(world) - 1 and 0 < c < len(row) - 1:
                if world[r][c] == "#" and world[r - 1][c] == "#" and world[r + 1][c] == "#" and world[r][
                    c - 1] == "#" and \
                        world[r][c + 1] == "#":
                    alignment_sum += abs(r - min_row) * abs(c - min_col)
    return alignment_sum


# print_world(world)

min_row, min_col = find_min_row_col(world)
alignment_sum = calculate_alignment_sum(world, min_row, min_col)
print("Part 1:", alignment_sum)


def print_path(world):
    n_cols = len(world[0])
    n_rows = len(world)

    r, c = [(r, row.index("^")) for r, row in enumerate(world) if "^" in row][0]

    direction = UP
    while True:
        dr, dc = get_dr_dc(direction)
        n_steps = 0

        while 0 <= r + dr < n_rows and 0 <= c + dc < n_cols and world[r + dr][c + dc] == "#":
            r, c = r + dr, c + dc
            n_steps += 1

        if n_steps:
            print(n_steps)
        if direction == RIGHT:
            if 0 <= r - 1 and world[r - 1][c] == "#":
                print("L", end=" ")
                direction = UP
            elif r + 1 < n_rows and world[r + 1][c] == "#":
                print("R", end=" ")
                direction = DOWN
            else:
                break
        elif direction == LEFT:
            if 0 <= r - 1 and world[r - 1][c] == "#":
                print("R", end=" ")
                direction = UP
            elif r + 1 < n_rows and world[r + 1][c] == "#":
                print("L", end=" ")
                direction = DOWN
            else:
                break
        elif direction == UP:
            if 0 <= c - 1 and world[r][c - 1] == "#":
                print("L", end=" ")
                direction = LEFT
            elif c - 1 < n_cols and world[r][c + 1] == "#":
                print("R", end=" ")
                direction = RIGHT
            else:
                break
        elif direction == DOWN:
            if 0 <= c - 1 and world[r][c - 1] == "#":
                print("R", end=" ")
                direction = LEFT
            elif c - 1 < n_cols and world[r][c + 1] == "#":
                print("L", end=" ")
                direction = RIGHT
            else:
                break


# print_path(world)

program[0] = 2
vm = VM(program)

current_c = 0


def input_provider():
    global current_c
    main_movement = "A,B,B,A,C,B,C,C,B,A\n"
    A = "R,10,R,8,L,10,L,10\n"
    B = "R,8,L,6,L,6\n"
    C = "L,10,R,10,L,6\n"
    for string in main_movement, A, B, C, "n\n":
        for c in string:
            yield ord(c)


provider = input_provider()
vm.get_input_callback = lambda: next(provider)

all_output = []
while True:
    try:
        all_output.append(vm.get_output())
    except StopIteration:
        break

print("Part 2", all_output[-1])
