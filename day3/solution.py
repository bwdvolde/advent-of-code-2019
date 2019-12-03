def read_file(path):
    with open(path, "r") as file:
        file_content = file.read()
        lines = file_content.splitlines()
        return [line.split(",") for line in lines]


def compute_intersections(commands_0, commands_1):
    return compute_positions(commands_0) & compute_positions(commands_1)


def position_diff(direction):
    if direction == "R":
        return 1, 0
    elif direction == "L":
        return -1, 0
    elif direction == "U":
        return 0, 1
    else:
        return 0, -1


def compute_positions(commands):
    positions = set()

    x, y = 0, 0
    for command in commands:
        direction = command[0]
        length = int(command[1:])
        dx, dy = position_diff(direction)
        for _ in range(length):
            x += dx
            y += dy
            position = (x, y)
            positions.add(position)
    return positions


def compute_steps(commands):
    position_to_steps = {}

    steps = 0
    x, y = 0, 0
    for command in commands:
        direction = command[0]
        length = int(command[1:])

        dx, dy = position_diff(direction)
        for _ in range(length):
            steps += 1
            x += dx
            y += dy
            position = (x, y)
            if position not in position_to_steps:
                position_to_steps[position] = steps

    return position_to_steps


if __name__ == "__main__":
    commands_0, commands_1 = read_file("input.txt")

    intersections = compute_intersections(commands_0, commands_1)

    manhattan_distances = [abs(x) + abs(y) for (x, y) in intersections]
    answer_1 = min(manhattan_distances)
    print("Part 1:", answer_1)

    steps_0, steps_1 = map(compute_steps, [commands_0, commands_1])
    steps_needed = [steps_0[intersection] + steps_1[intersection] for intersection in intersections]
    answer_2 = min(steps_needed)
    print("Part 2:", answer_2)
