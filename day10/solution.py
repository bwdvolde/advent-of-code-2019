import math

from intcode import intcode


def read_file(path):
    with open(path, "r") as file:
        file_content = file.read()
        lines = file_content.split("\n")
        return lines


def make_coordinates(lines):
    return [(x, y)
            for y, line in enumerate(lines)
            for x, c in enumerate(line)
            if c == "#"]


def compute_angle(a, b):
    dx = a[0] - b[0]
    dy = a[1] - b[1]
    angle = math.atan2(dx, dy)
    if angle > 0:
        angle -= math.pi * 2
    return angle


def compute_n_visible_asteroids(self, coordinates):
    angles = set()
    visible_coordinates = []
    for other in coordinates:
        if self != other:
            angle = compute_angle(self, other)
            if angle not in angles:
                visible_coordinates.append(other)
            angles.add(angle)

    return visible_coordinates


if __name__ == "__main__":
    lines = read_file("input.txt")

    coordinates = make_coordinates(lines)

    best_coordinate, visible_coordinates = max(
        [(coordinate, compute_n_visible_asteroids(coordinate, coordinates)) for coordinate in coordinates],
        key=lambda a: len(a[1]))

    print("Part 1:", len(visible_coordinates))

    sorted_coordinates = sorted(visible_coordinates,
                                key=lambda visible_coordinate: compute_angle(best_coordinate, visible_coordinate),
                                reverse=True)

    print("Part 2:", sorted_coordinates[199])
