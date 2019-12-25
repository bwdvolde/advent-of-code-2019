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


def read_program(path):
    with open(path, "r") as file:
        file_content = file.read()
        lines = file_content.split(",")
        return list(map(int, lines))


class VM:

    def __init__(self, state):
        self.ip = 0
        self.relative_base = 0
        self.state = state

        self.state_map = defaultdict(lambda: 0)
        for i, value in enumerate(state):
            self.state_map[i] = value

        self.get_input_callback = lambda: int(input("Input: "))

    def get_output(self):
        return self.continue_program()

    def get_ascii_output(self):
        output = self.continue_program()
        try:
            return chr(output)
        except ValueError:
            return output

    def set_input(self, input):
        self.get_input_callback = lambda: input

    def set_input_generator(self, generator):
        self.get_input_callback = lambda: next(generator)

    def set_input_string(self, input_string):
        self.set_input_strings([input_string])

    def set_input_strings(self, input_strings):
        def generator():
            for string in input_strings:
                for c in string:
                    yield ord(c)

        gen = generator()
        self.get_input_callback = lambda: next(gen)

    def continue_program(self):
        while self.state_map[self.ip] != OPCODE_STOP:
            opcode = self.state_map[self.ip]
            instruction = opcode % 100

            mode_0 = opcode // 100 % 10
            mode_1 = opcode // 1000 % 10
            mode_2 = opcode // 10000 % 10

            if instruction == OPCODE_INPUT:
                store_address = self._get_store_addres(0, mode_0)
                self.state_map[store_address] = self.get_input_callback()
                self.ip += 2
            elif instruction == OPCODE_OUTPUT:
                output = self._get_parameter(0, mode_0)
                self.ip += 2
                return output
            else:
                parameter_0 = self._get_parameter(0, mode_0)
                parameter_1 = self._get_parameter(1, mode_1)
                parameter_2 = self._get_store_addres(2, mode_2)

                if instruction == OPCODE_ADDITION:
                    self.state_map[parameter_2] = parameter_0 + parameter_1
                    self.ip += 4
                elif instruction == OPCODE_MULTIPLICATION:
                    self.state_map[parameter_2] = parameter_0 * parameter_1
                    self.ip += 4
                elif instruction == OPCODE_JUMP_IF_TRUE:
                    self.ip += 3
                    if parameter_0:
                        self.ip = parameter_1
                elif instruction == OPCODE_JUMP_IF_FALSE:
                    self.ip += 3
                    if not parameter_0:
                        self.ip = parameter_1
                elif instruction == OPCODE_LESS_THAN:
                    self.state_map[parameter_2] = int(parameter_0 < parameter_1)
                    self.ip += 4
                elif instruction == OPCODE_EQUALS:
                    self.state_map[parameter_2] = int(parameter_0 == parameter_1)
                    self.ip += 4
                elif instruction == OPCODE_RELATIVE_BASE:
                    self.relative_base += parameter_0
                    self.ip += 2

        raise StopIteration

    def _get_parameter(self, i, mode):
        param = self.state_map[self.ip + i + 1]
        if mode == MODE_POSITION:
            return self.state_map[param]
        elif mode == MODE_IMMEDIATE:
            return param
        else:
            return self.state_map[param + self.relative_base]

    def _get_store_addres(self, i, mode):
        store_address = self._get_parameter(i, MODE_IMMEDIATE)
        if mode == MODE_RELATIVE:
            store_address += self.relative_base
        return store_address
