from intcode.intcode import read_program, VM

TILE_EMPTY = 0
TILE_WALL = 1
TILE_BLOCK = 2
TILE_HORIZONTAL_PADDLE = 3
TILE_BALL = 4

characters = {
    TILE_EMPTY: " ",
    TILE_WALL: "W",
    TILE_BLOCK: "□",
    TILE_HORIZONTAL_PADDLE: "-",
    TILE_BALL: "O"
}


def read_initial_tiles(vm):
    tiles = []
    while True:
        try:
            col = vm.get_output()
            row = vm.get_output()
            tile_id = vm.get_output()

            if col == -1:
                break

            tiles.append((col, row, tile_id))

        except StopIteration:
            break

    return tiles


def create_board(tiles):
    max_col = max(tile[0] for tile in tiles)
    max_row = max(tile[1] for tile in tiles)

    board = [[0 for _ in range(max_col + 1)] for _ in range(max_row + 1)]

    for tile in tiles:
        col, row, tile_id = tile
        board[row][col] = tile_id

    return board


def print_board(board, score):
    for row in board:
        for tile_id in row:
            c = characters[tile_id]
            print(c, end="")
        print()

    print("Score:", score)


def calculate_move(col_paddle, col_ball):
    if col_paddle < col_ball:
        return 1
    elif col_paddle > col_ball:
        return -1
    return 0


program = read_program("input.txt")

vm = VM(program)
tiles = read_initial_tiles(vm)
n_block_tiles = len([_ for _, _, tile_id in tiles if tile_id == TILE_BLOCK])
print("Part 1:", n_block_tiles)


program[0] = 2
vm = VM(program)

tiles = read_initial_tiles(vm)
board = create_board(tiles)

col_paddle = next(tile for tile in tiles if tile[2] == TILE_HORIZONTAL_PADDLE)[0]
col_ball = next(tile for tile in tiles if tile[2] == TILE_BALL)[0]
vm.get_input_callback = lambda: calculate_move(col_paddle, col_ball)

score = 0

while True:
    try:
        col = vm.get_output()
        row = vm.get_output()
        tile_id = vm.get_output()

        if col == -1:
            score = tile_id
        else:
            if tile_id == TILE_HORIZONTAL_PADDLE:
                col_paddle = col
            if tile_id == TILE_BALL:
                col_ball = col
            board[row][col] = tile_id
    except StopIteration:
        break

print("Part 2:", score)
