from collections import deque

from intcode.intcode import read_program, VM

NORTH = 1
SOUTH = 2
WEST = 3
EAST = 4

DIRECTIONS = [NORTH, SOUTH, EAST, WEST]
INVERSE_DIRECTIONS = {
    NORTH: SOUTH,
    SOUTH: NORTH,
    EAST: WEST,
    WEST: EAST
}

RESPONSE_HIT_WALL = 0
RESPONSE_MOVED = 1
RESPONSE_FOUND = 2

D_POSITION = {
    NORTH: (0, -1),
    SOUTH: (0, 1),
    WEST: (1, 0),
    EAST: (-1, 0)
}


def calculate_next_position(position, direction):
    x, y = position
    dx, dy = D_POSITION[direction]
    return x + dx, y + dy


def inverse_direction(direction):
    return [SOUTH, NORTH, WEST, EAST][direction]


def discover_area():
    program = read_program("input.txt")
    vm = VM(program)

    oxygen_position = None
    blocked_positions = set()
    free_positions = set()

    def recursive_discover(current_position):
        nonlocal oxygen_position

        if current_position in free_positions:
            return
        free_positions.add(current_position)

        for direction in DIRECTIONS:
            next_position = calculate_next_position(current_position, direction)
            if next_position not in blocked_positions:
                vm.set_input(direction)
                response = vm.get_output()

                if response == RESPONSE_HIT_WALL:
                    blocked_positions.add(next_position)
                else:
                    if response == RESPONSE_FOUND:
                        oxygen_position = next_position
                    recursive_discover(next_position)

                    # Go back to current position
                    vm.set_input(INVERSE_DIRECTIONS[direction])
                    assert vm.get_output() != 0

    recursive_discover((0, 0))
    return free_positions, oxygen_position


def find_distances_from(positions, start):
    distances = {}
    queue = deque([(start, 0)])
    while queue:
        position, distance = queue.popleft()
        distances[position] = distance

        for direction in DIRECTIONS:
            next_position = calculate_next_position(position, direction)
            if next_position in positions and next_position not in distances.keys():
                queue.append((next_position, distance + 1))

    return distances


positions, oxygen_position = discover_area()

distances_from_start = find_distances_from(positions, (0, 0))
print("Part 1:", distances_from_start[oxygen_position])

distances_from_oxygen = find_distances_from(positions, oxygen_position)
print("Part 2:", max(distances_from_oxygen.values()))
