def read_file(path):
    with open(path, "r") as file:
        file_content = file.read()
        lines = file_content.split(",")
        return list(map(int, lines))


OPCODE_ADDITION = 1
OPCODE_MULTIPLICATION = 2
OPCODE_STOP = 99


def process(state):
    i = 0
    while state[i] != OPCODE_STOP:
        opcode = state[i]

        left_operand = state[i + 1]
        right_operand = state[i + 2]
        destination = state[i + 3]

        if opcode == OPCODE_ADDITION:
            state[destination] = state[left_operand] + state[right_operand]
        else:
            state[destination] = state[left_operand] * state[right_operand]

        i += 4

    return state


def compute_output(initial_state, noun, verb):
    state = initial_state[:]
    state[1] = noun
    state[2] = verb

    return process(state)[0]


def find_combination(initial_state, desired_output):
    for noun in range(100):
        for verb in range(100):
            output = compute_output(initial_state, noun, verb)
            if output == desired_output:
                return noun, verb
            elif output > desired_output:
                break


if __name__ == "__main__":
    initial_state = read_file("input.txt")
    output = compute_output(initial_state, 12, 2)
    print("Part 1:", output)

    noun, verb = find_combination(initial_state, 19690720)
    answer = 100 * noun + verb
    print("Part 2:", answer)


