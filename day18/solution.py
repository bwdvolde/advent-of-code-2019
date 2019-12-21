from collections import deque

from read_file.read_file import read_file

lines = read_file("input.txt")[:-1]
lines = """########################
#...............b.C.D.f#
#.######################
#.....@.a.B.c.d.A.e.F.g#
########################""".split("\n")

world = [list(line) for line in lines]

start_pos = None
n_keys = 0
n_doors = 0
key_positions = {}
for r, row in enumerate(world):
    for c, char in enumerate(row):
        if char == "@":
            start_pos = (r, c)
        elif char.islower():
            n_keys += 1
            key_positions[char] = (r, c)
        elif char.isupper():
            n_doors += 1

print(start_pos, n_keys, n_doors)


def find_possible_keys(pos, opened_doors):
    queue = deque([(pos, 0)])
    visited = {pos}
    possible_keys = []
    while queue:
        pos, distance = queue.popleft()
        r, c = pos
        for (dr, dc) in [(-1, 0), (1, 0), (0, -1), (0, 1)]:
            neighbor = world[r + dr][c + dc]
            neighbor_pos = (r + dr, c + dc)
            if (neighbor in [".", "@"] or neighbor.upper() in opened_doors) and neighbor_pos not in visited:
                queue.append((neighbor_pos, distance + 1))
                visited.add(neighbor_pos)
            elif neighbor.islower() and neighbor.upper() not in opened_doors:
                possible_keys.append((neighbor, distance + 1))
    return possible_keys


def find_shortest_path(world, start_pos):
    lowest_steps = 10 ** 10

    def back_track(pos, current_path, current_steps):
        nonlocal lowest_steps

        if current_steps + 6 > lowest_steps:
            return

        if len(current_path) == n_keys and current_steps < lowest_steps:
            lowest_steps = current_steps
            print(lowest_steps, current_path)

        opened_doors = {key.upper() for key in current_path}
        possible_keys = find_possible_keys(pos, opened_doors)

        possible_steps_needed = [a[1] for a in possible_keys]
        if not possible_steps_needed or max(possible_steps_needed) - min(
                possible_steps_needed) + current_steps > lowest_steps:
            return

        possible_keys.sort(key=lambda a: a[1])
        for (key, steps_needed) in possible_keys:
            key_pos = key_positions[key]
            back_track(key_pos, current_path + [key], current_steps + steps_needed)

    back_track(start_pos, [], 0)
    print(lowest_steps)


find_shortest_path(world, start_pos)
