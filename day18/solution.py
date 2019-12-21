import time
from collections import deque
from functools import lru_cache

from read_file.read_file import read_file

lines = read_file("input.txt")[:-1]
# lines = """#################
# #i.G..c...e..H.p#
# ########.########
# #j.A..b...f..D.o#
# ########@########
# #k.E..a...g..B.n#
# ########.########
# #l.F..d...h..C.m#
# #################""".split("\n")

world = [list(line) for line in lines]

start_pos = None
keys = set()
n_doors = 0
key_positions = {}
for r, row in enumerate(world):
    for c, char in enumerate(row):
        if char == "@":
            start_pos = (r, c)
            key_positions[char] = (r, c)
        elif char.islower():
            keys.add(char)
            key_positions[char] = (r, c)
        elif char.isupper():
            n_doors += 1

print(start_pos, keys, n_doors)


def find_distances(start_pos):
    queue = deque([(start_pos, 0, set())])
    visited = {start_pos}
    distances = []
    while queue:
        start_pos, distance, doors_on_path = queue.popleft()
        r, c = start_pos

        current = world[r][c]
        if current.isupper():
            doors_on_path = doors_on_path | {current.lower()}

        for (dr, dc) in [(-1, 0), (1, 0), (0, -1), (0, 1)]:
            neighbor = world[r + dr][c + dc]
            neighbor_pos = (r + dr, c + dc)
            if neighbor != "#" and neighbor_pos not in visited:
                queue.append((neighbor_pos, distance + 1, doors_on_path))
                visited.add(neighbor_pos)
                if neighbor.islower():
                    distances.append((neighbor, distance + 1, doors_on_path))
    return distances


key_to_distances = {}
for key in ["@"] + list(keys):
    key_to_distances[key] = find_distances(key_positions[key])


def find_shortest_steps(start_pos):
    cache = {}

    def calculate_required_steps(current_key, remaining_keys):
        if not remaining_keys:
            return 0

        cache_key = current_key + "".join(remaining_keys)
        if cache_key in cache:
            return cache[cache_key]

        lowest_required_steps = float("inf")
        for (key, steps, required_opened_doors) in key_to_distances[current_key]:
            if steps > lowest_required_steps:
                continue
            elif required_opened_doors & remaining_keys: # Not all doors have been opened
                continue
            elif key not in remaining_keys: # Key has already been selected
                continue
            else:
                required_steps = calculate_required_steps(key, remaining_keys - {key}) + steps
                lowest_required_steps = min(lowest_required_steps, required_steps)

        cache[cache_key] = lowest_required_steps
        return lowest_required_steps

    return calculate_required_steps("@", keys)



find_shortest_steps(start_pos)
