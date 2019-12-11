import itertools

from day07 import intcode


def read_file(path):
    with open(path, "r") as file:
        file_content = file.read()
        lines = file_content.split(",")
        return list(map(int, lines))


def find_highest_signal(program, possible_phase_settings):
    permutations = itertools.permutations(possible_phase_settings)
    return max(compute_output_signal(phase_settings, program) for phase_settings in permutations)


def compute_output_signal(phase_settings, program):
    amplifiers = []
    for phase_setting in phase_settings:
        amplifier = intcode.run(program)
        amplifiers.append(amplifier)

        # Pass phase setting
        next(amplifier)
        amplifier.send(phase_setting)

    input_signal = 0
    halted = False
    while not halted:
        for amplifier in amplifiers:
            try:
                input_signal = amplifier.send(input_signal)
                next(amplifier)
            except StopIteration:
                halted = True

    return input_signal


if __name__ == "__main__":
    program = read_file("input.txt")
    print("Part 1:", find_highest_signal(program, [0, 1, 2, 3, 4]))
    print("Part 2:", find_highest_signal(program, [5, 6, 7, 8, 9]))
