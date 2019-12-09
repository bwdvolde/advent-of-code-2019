from intcode import intcode


def read_file(path):
    with open(path, "r") as file:
        file_content = file.read()
        lines = file_content.split(",")
        return list(map(int, lines))


if __name__ == "__main__":
    initial_state = read_file("input.txt")
    intcode.process(initial_state)
