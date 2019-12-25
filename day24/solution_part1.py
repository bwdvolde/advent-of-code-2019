from collections import Counter

from read_file.read_file import read_file

lines = read_file("input.txt")[:-1]
from copy import deepcopy

BUG = "#"
EMPTY = "."

# lines = """.....
# .....
# .....
# #....
# .#...""".split("\n")

world = [list(line) for line in lines]


def print_world(world):
    for row in world:
        for char in row:
            print(char, end="")
        print()


def find_neighbors(world, coordinate):
    r, c = coordinate
    neighbor_coordinates = [(r + dr, c + dc) for (dr, dc) in [(-1, 0), (1, 0), (0, -1), (0, 1)] if
                            0 <= r + dr < len(world) and 0 <= c + dc < len(world[0])]

    return [world[nr][nc] for (nr, nc) in neighbor_coordinates]


def calculate_next_world(world):
    next_world = deepcopy(world)
    for r, row in enumerate(world):
        for c, char in enumerate(row):
            current_char = world[r][c]
            neighbor_chars = find_neighbors(world, (r, c))
            counts = Counter(neighbor_chars)
            if current_char == BUG and counts[BUG] != 1:
                next_world[r][c] = EMPTY
            elif current_char == EMPTY and counts[BUG] in [1, 2]:
                next_world[r][c] = BUG
    return next_world


def calculate_biodiversity_score(world):
    flattened = [char for row in world for char in row]
    bug_indices = [i for i, char in enumerate(flattened) if char == BUG]
    return sum(2 ** i for i in bug_indices)


previous_worlds = [world]
world = calculate_next_world(world)
while not any(world == previous_world for previous_world in previous_worlds):
    previous_worlds.append(world)
    world = calculate_next_world(world)

print("Part 1:", calculate_biodiversity_score(world))
