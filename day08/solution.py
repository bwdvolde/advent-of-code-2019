import numpy as np


def read_file(path):
    with open(path, "r") as file:
        file_content = file.read()
        file_content = file_content.rstrip("\n")
        return [int(char) for char in file_content]


def combine_layers(layers):
    result = np.zeros((height, width), dtype=int)
    for row in range(height):
        for col in range(width):
            i = 0
            while i < len(layers) and layers[i][row][col] == 2:
                i += 1
            result[row][col] = layers[i][row][col]
    return result


def print_image(result):
    for row in range(height):
        for col in range(width):
            pixel = result[row][col]
            if pixel == 1:
                print("X", end="")
            else:
                print(" ", end="")
        print()


if __name__ == "__main__":
    colors = read_file("input.txt")
    print(colors)

    width = 25
    height = 6

    layer_size = width * height
    layers = [colors[i:i + layer_size] for i in range(0, len(colors), layer_size)]
    layers = [np.resize(layer, (height, width)) for layer in layers]
    counts = [np.unique(layer, return_counts=True)[1] for layer in layers]

    index = min(range(len(layers)), key=lambda i: counts[i][0])
    counts = counts[index]
    print("Part 1:", counts[1] * counts[2])

    result = combine_layers(layers)
    print("Part 2:")
    print_image(result)
