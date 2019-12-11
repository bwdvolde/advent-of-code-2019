from collections import defaultdict

from intcode.intcode import read_program, VM
import matplotlib.pyplot as plt

DIRECTION_LEFT = (-1, 0)
DIRECTION_RIGHT = (1, 0)
DIRECTION_UP = (0, -1)
DIRECTION_DOWN = (0, 1)

TURN_LEFT = 0
TURN_RIGHT = 1

COLOR_BLACK = 0
COLOR_WHITE = 1

next_direction_left = {
    DIRECTION_UP: DIRECTION_LEFT,
    DIRECTION_LEFT: DIRECTION_DOWN,
    DIRECTION_DOWN: DIRECTION_RIGHT,
    DIRECTION_RIGHT: DIRECTION_UP
}

next_direction_right = {
    DIRECTION_UP: DIRECTION_RIGHT,
    DIRECTION_RIGHT: DIRECTION_DOWN,
    DIRECTION_DOWN: DIRECTION_LEFT,
    DIRECTION_LEFT: DIRECTION_UP
}


def compute_position_to_color(initial_state, inital_color):
    position_to_color = defaultdict(lambda: COLOR_BLACK)

    position = (0, 0)
    direction = DIRECTION_UP
    position_to_color[position] = inital_color

    vm = VM(initial_state)
    running = True
    while running:
        try:
            current_color = position_to_color[position]
            vm.send_input(current_color)

            color = vm.get_output()
            turn = vm.get_output()

            position_to_color[position] = color
            direction = next_direction(direction, turn)
            position = next_position(position, direction)

        except StopIteration:
            running = False

    return position_to_color


def next_direction(current_direction, turn):
    if turn == TURN_LEFT:
        return next_direction_left[current_direction]
    else:
        return next_direction_right[current_direction]


def next_position(position, direction):
    dx, dy = direction
    x, y = position
    return (x + dx, y + dy)


def draw(position_to_color):
    white_positions = [position for position, color in position_to_color.items() if color == COLOR_WHITE]
    x, y = zip(*white_positions)
    plt.scatter(x, y, s=20)
    plt.ylim((10, -20))
    plt.show()


if __name__ == "__main__":
    initial_state = read_program("input.txt")

    position_to_color = compute_position_to_color(initial_state, COLOR_BLACK)
    print("Part 1:", len(position_to_color))

    position_to_color = compute_position_to_color(initial_state, COLOR_WHITE)
    draw(position_to_color)
