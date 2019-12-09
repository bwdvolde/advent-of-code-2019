from collections import defaultdict

MODE_POSITION = 0
MODE_IMMEDIATE = 1
MODE_RELATIVE = 2

OPCODE_ADDITION = 1
OPCODE_MULTIPLICATION = 2
OPCODE_INPUT = 3
OPCODE_OUTPUT = 4
OPCODE_JUMP_IF_TRUE = 5
OPCODE_JUMP_IF_FALSE = 6
OPCODE_LESS_THAN = 7
OPCODE_EQUALS = 8
OPCODE_RELATIVE_BASE = 9
OPCODE_STOP = 99


def process(state):
    state_map = defaultdict(lambda: 0)
    for i, value in enumerate(state):
        state_map[i] = value

    ip = 0
    relative_base = 0

    def get_parameter(i, mode):
        param = state_map[ip + i + 1]
        if mode == MODE_POSITION:
            return state_map[param]
        elif mode == MODE_IMMEDIATE:
            return param
        else:
            return state_map[param + relative_base]

    def get_store_addres(i, mode):
        store_address = get_parameter(i, MODE_IMMEDIATE)
        if mode == MODE_RELATIVE:
            store_address += relative_base
        return store_address

    while state_map[ip] != OPCODE_STOP:
        opcode = state_map[ip]
        instruction = opcode % 100

        mode_0 = opcode // 100 % 10
        mode_1 = opcode // 1000 % 10
        mode_2 = opcode // 10000 % 10

        if instruction == OPCODE_INPUT:
            store_address = get_store_addres(0, mode_0)
            state_map[store_address] = int(input())
            ip += 2
        elif instruction == OPCODE_OUTPUT:
            output = get_parameter(0, mode_0)
            print(output)
            ip += 2
        else:
            parameter_0 = get_parameter(0, mode_0)
            parameter_1 = get_parameter(1, mode_1)
            parameter_2 = get_store_addres(2, mode_2)

            if instruction == OPCODE_ADDITION:
                state_map[parameter_2] = parameter_0 + parameter_1
                ip += 4
            elif instruction == OPCODE_MULTIPLICATION:
                state_map[parameter_2] = parameter_0 * parameter_1
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
                state_map[parameter_2] = int(parameter_0 < parameter_1)
                ip += 4
            elif instruction == OPCODE_EQUALS:
                state_map[parameter_2] = int(parameter_0 == parameter_1)
                ip += 4
            elif instruction == OPCODE_RELATIVE_BASE:
                relative_base += parameter_0
                ip += 2

    return state_map
