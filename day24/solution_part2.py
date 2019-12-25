from read_file.read_file import read_file

lines = read_file("input.txt")[:-1]

BUG = "#"
EMPTY = "."


def find_neighbor_coordinates(coordinate):
    r, c, depth = coordinate

    neighbor_coordinates = []

    # Outer neighbors
    if r == 0:
        neighbor_coordinates.append((1, 2, depth - 1))
    if c == 0:
        neighbor_coordinates.append((2, 1, depth - 1))
    if r == 4:
        neighbor_coordinates.append((3, 2, depth - 1))
    if c == 4:
        neighbor_coordinates.append((2, 3, depth - 1))

    # Inner neighbours
    if (r, c) == (1, 2):
        neighbor_coordinates += [(0, nc, depth + 1) for nc in range(5)]
    if (r, c) == (3, 2):
        neighbor_coordinates += [(4, nc, depth + 1) for nc in range(5)]
    if (r, c) == (2, 1):
        neighbor_coordinates += [(nr, 0, depth + 1) for nr in range(5)]
    if (r, c) == (2, 3):
        neighbor_coordinates += [(nr, 4, depth + 1) for nr in range(5)]

    neighbor_coordinates += [(r + dr, c + dc, depth) for (dr, dc) in [(-1, 0), (1, 0), (0, -1), (0, 1)] if
                             0 <= r + dr < 5 and 0 <= c + dc < 5 and (r + dr, c + dc) != (2, 2)]

    return neighbor_coordinates


def find_next_bug_coordinates(bug_coordinates):
    new_bug_coordinates = set()
    for bug_coordinate in bug_coordinates:
        bug_neighbor_coordinates = find_neighbor_coordinates(bug_coordinate)
        for coordinate in [bug_coordinate, *bug_neighbor_coordinates]:
            neighbor_coordinates = find_neighbor_coordinates(coordinate)
            is_bug = coordinate in bug_coordinates
            n_adjacent_bugs = sum(
                1 for neighbor_coordinate in neighbor_coordinates if neighbor_coordinate in bug_coordinates)

            if (is_bug and n_adjacent_bugs == 1) or (not is_bug and n_adjacent_bugs in [1, 2]):
                new_bug_coordinates.add(coordinate)
    return new_bug_coordinates


def print_bug_coordinates(bug_coordinates):
    for r in range(5):
        for c in range(5):
            if (r, c, 0) in bug_coordinates:
                print("#", end="")
            else:
                print(".", end="")
        print()


world = [list(line) for line in lines]
bug_coordinates = {(r, c, 0) for r, row in enumerate(world) for c, char in enumerate(row) if char == BUG}

n_minutes = 200
for _ in range(n_minutes):
    bug_coordinates = find_next_bug_coordinates(bug_coordinates)

print("Part 2:", len(bug_coordinates))
