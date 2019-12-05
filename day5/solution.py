def read_file(path):
    with open(path, "r") as file:
        file_content = file.read()
        lines = file_content.split(",")
        return list(map(int, lines))


OPCODE_ADDITION = 1
OPCODE_MULTIPLICATION = 2
OPCODE_INPUT = 3
OPCODE_OUTPUT = 4
OPCODE_JUMP_IF_TRUE = 5
OPCODE_JUMP_IF_FALSE = 6
OPCODE_LESS_THAN = 7
OPCODE_EQUALS = 8
OPCODE_STOP = 99


def process(state):
    ip = 0
    while state[ip] != OPCODE_STOP:
        opcode = state[ip]
        instruction = opcode % 100

        parameter_0_immediate_mode = opcode // 100 & 1
        parameter_1_immediate_mode = opcode // 1000 & 1

        if instruction == OPCODE_INPUT:
            store_address = state[ip + 1]
            state[store_address] = int(input())
            ip += 2
        elif instruction == OPCODE_OUTPUT:
            parameter = state[ip + 1]
            output = parameter if parameter_0_immediate_mode else state[parameter]
            print(output)
            ip += 2
        else:
            parameter_0 = state[ip + 1] if parameter_0_immediate_mode else state[state[ip + 1]]
            parameter_1 = state[ip + 2] if parameter_1_immediate_mode else state[state[ip + 2]]
            parameter_2 = state[ip + 3]

            if instruction == OPCODE_ADDITION:
                state[parameter_2] = parameter_0 + parameter_1
                ip += 4
            elif instruction == OPCODE_MULTIPLICATION:
                state[parameter_2] = parameter_0 * parameter_1
                ip += 4
            elif instruction == OPCODE_JUMP_IF_TRUE:
                ip += 3
                if parameter_0:
                    ip = parameter_1
            elif instruction == OPCODE_JUMP_IF_FALSE:
                ip += 3
                if not parameter_0:
                    ip = parameter_1
            elif instruction == OPCODE_LESS_THAN:
                state[parameter_2] = int(parameter_0 < parameter_1)
                ip += 4
            elif instruction == OPCODE_EQUALS:
                state[parameter_2] = int(parameter_0 == parameter_1)
                ip += 4

    return state


if __name__ == "__main__":
    initial_state = read_file("input.txt")
    process(initial_state)
