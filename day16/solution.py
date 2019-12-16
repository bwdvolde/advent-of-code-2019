import itertools
import numpy as np

BASE_PATTERN = [0, 1, 0, -1]


def read_file(path):
    with open(path, "r") as file:
        file_content = file.read()
        file_content = file_content.rstrip("\n")
    return file_content


def get_pattern(i):
    base_i = 0
    first = True
    while True:
        for j in range(i + 1):
            if not first:
                yield BASE_PATTERN[base_i]
            first = False
        base_i = (base_i + 1) % len(BASE_PATTERN)


input_string = read_file("input.txt")
input_signal = np.array([int(c) for c in input_string])

patterns = []
for i in range(len(input_string)):
    pattern = list(itertools.islice(get_pattern(i, ), len(input_string)))
    pattern = np.array(pattern)
    patterns.append(pattern)

n_phases = 100
for _ in range(n_phases):
    output_signal = []
    for i in range(len(input_signal)):
        output_value = np.sum(input_signal * patterns[i])
        output_value = abs(output_value) % 10
        output_signal.append(output_value)

    input_signal = output_signal

print("Part 1:", input_signal[:8])

### PART 2

input_string *= 10000
input_signal = np.array([int(c) for c in input_string])

digits_to_skip = int("".join(map(str, input_signal[:7])))
input_signal = input_signal[digits_to_skip:]

n_phases = 100
for _ in range(n_phases):
    output_signal = []
    total_sum = sum(input_signal)
    for _, value in enumerate(input_signal):
        output_value = abs(total_sum) % 10
        output_signal.append(output_value)
        total_sum -= value
    input_signal = output_signal

print("Part 2:", input_signal[:8])
