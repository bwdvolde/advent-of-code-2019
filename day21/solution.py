from intcode.intcode import read_program, VM

program = read_program("input.txt")
vm = VM(program)

script = """OR G J
OR I J
AND E J
OR H J
AND D J
OR A T
AND B T
AND C T
NOT T T
AND T J
NOT A T
OR T J
RUN
"""
vm.set_input_strings(script)

while True:
    try:
        print(vm.get_ascii_output(), end="")
    except StopIteration:
        break
