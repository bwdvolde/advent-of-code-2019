from intcode.intcode import read_program, VM
import math

program = read_program("input.txt")

height = 10
width = 10


def get_output_for(x, y):
    vm = VM(program)

    def create_generator():
        yield x
        yield y

    generator = create_generator()
    vm.get_input_callback = lambda: next(generator)
    return vm.get_output()


n_affected_points = sum(get_output_for(x, y) for x in range(50) for y in range(50))
print("Part 1:", n_affected_points)

y = 0
x = 0
while not get_output_for(x + 99, y):
    y += 1
    while not get_output_for(x, y + 99):
        x += 1

print("Part 2:", x, y)
