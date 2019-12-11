OPCODE_ADDITION = 1
OPCODE_MULTIPLICATION = 2
OPCODE_INPUT = 3
OPCODE_OUTPUT = 4
OPCODE_JUMP_IF_TRUE = 5
OPCODE_JUMP_IF_FALSE = 6
OPCODE_LESS_THAN = 7
OPCODE_EQUALS = 8
OPCODE_STOP = 99


def run(program):
    program = program[:]
    ip = 0
    while program[ip] != OPCODE_STOP:
        opcode = program[ip]
        instruction = opcode % 100

        parameter_0_immediate_mode = opcode // 100 & 1
        parameter_1_immediate_mode = opcode // 1000 & 1

        if instruction == OPCODE_INPUT:
            store_address = program[ip + 1]
            input_value = yield
            program[store_address] = input_value
            ip += 2
        elif instruction == OPCODE_OUTPUT:
            parameter = program[ip + 1]
            output = parameter if parameter_0_immediate_mode else program[parameter]
            yield output
            ip += 2
        else:
            parameter_0 = program[ip + 1] if parameter_0_immediate_mode else program[program[ip + 1]]
            parameter_1 = program[ip + 2] if parameter_1_immediate_mode else program[program[ip + 2]]
            parameter_2 = program[ip + 3]

            if instruction == OPCODE_ADDITION:
                program[parameter_2] = parameter_0 + parameter_1
                ip += 4
            elif instruction == OPCODE_MULTIPLICATION:
                program[parameter_2] = parameter_0 * parameter_1
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
                program[parameter_2] = int(parameter_0 < parameter_1)
                ip += 4
            elif instruction == OPCODE_EQUALS:
                program[parameter_2] = int(parameter_0 == parameter_1)
                ip += 4

    return program
