from collections import defaultdict, deque

from read_file import read_file

world = """
             Z L X W       C                 
             Z P Q B       K                 
  ###########.#.#.#.#######.###############  
  #...#.......#.#.......#.#.......#.#.#...#  
  ###.#.#.#.#.#.#.#.###.#.#.#######.#.#.###  
  #.#...#.#.#...#.#.#...#...#...#.#.......#  
  #.###.#######.###.###.#.###.###.#.#######  
  #...#.......#.#...#...#.............#...#  
  #.#########.#######.#.#######.#######.###  
  #...#.#    F       R I       Z    #.#.#.#  
  #.###.#    D       E C       H    #.#.#.#  
  #.#...#                           #...#.#  
  #.###.#                           #.###.#  
  #.#....OA                       WB..#.#..ZH
  #.###.#                           #.#.#.#  
CJ......#                           #.....#  
  #######                           #######  
  #.#....CK                         #......IC
  #.###.#                           #.###.#  
  #.....#                           #...#.#  
  ###.###                           #.#.#.#  
XF....#.#                         RF..#.#.#  
  #####.#                           #######  
  #......CJ                       NM..#...#  
  ###.#.#                           #.###.#  
RE....#.#                           #......RF
  ###.###        X   X       L      #.#.#.#  
  #.....#        F   Q       P      #.#.#.#  
  ###.###########.###.#######.#########.###  
  #.....#...#.....#.......#...#.....#.#...#  
  #####.#.###.#######.#######.###.###.#.#.#  
  #.......#.......#.#.#.#.#...#...#...#.#.#  
  #####.###.#####.#.#.#.#.###.###.#.###.###  
  #.......#.....#.#...#...............#...#  
  #############.#.#.###.###################  
               A O F   N                     
               A A D   M                     """.split("\n")[1:]

world = read_file.read_file("input.txt")[:-1]
world = [list(row) for row in world]


# Find portal positions and merge characters into 1 string to make our life easier
def calculate_portal_positions(world):
    portal_positions = defaultdict(list)
    for r, row in enumerate(world):
        for c, char in enumerate(row):
            if len(char) == 1 and char.isupper():
                if r + 1 < len(world) and world[r + 1][c] == ".":
                    world[r][c] += world[r - 1][c]
                    world[r - 1][c] = " "
                elif r - 1 >= 0 and world[r - 1][c] == ".":
                    world[r][c] += world[r + 1][c]
                    world[r + 1][c] = " "
                elif c + 1 < len(row) and world[r][c + 1] == ".":
                    world[r][c] += world[r][c - 1]
                    world[r][c - 1] = " "
                elif c - 1 >= 0 and world[r][c - 1] == ".":
                    world[r][c] += world[r][c + 1]
                    world[r][c + 1] = " "

                if len(world[r][c]) == 2:
                    world[r][c] = "".join(sorted(world[r][c]))
                    portal_positions[world[r][c]].append((r, c))

    return portal_positions


def calculate_teleport_position(portal_positions):
    teleport_position = {}
    for name, positions in portal_positions.items():
        if name not in ["AA", "ZZ"]:
            a, b = positions
            teleport_position[a] = b
            teleport_position[b] = a

    return teleport_position


def is_portal(char):
    return len(char) == 2


def is_outer_portal(position, world):
    r, c = position
    return r == 1 or c == 1 or r == len(world) - 2 or c == len(world[0]) - 2


portal_positions = calculate_portal_positions(world)
teleport_position = calculate_teleport_position(portal_positions)

print(portal_positions)
print(teleport_position)

start_position = portal_positions["AA"][0]
end_position = portal_positions["ZZ"][0]

queue = deque([(start_position, 0, 0)])
visited = set()
while queue:
    position, distance, dimension = queue.popleft()
    r, c = position
    char = world[r][c]

    for dr, dc in [(-1, 0), (1, 0), (0, -1), (0, 1)]:
        next_char = world[r + dr][c + dc]
        next_position = (r + dr, c + dc)
        next_distance = distance if len(char) == 2 else distance + 1
        next_dimension = dimension

        if (dimension, next_position) not in visited and (next_char == "." or is_portal(next_char)):
            if next_char == "AA" or (next_char == "ZZ" and dimension != 0):
                continue
            elif next_char == "ZZ":
                print("Part 2:", distance)
                exit()
            elif is_portal(next_char):
                if is_outer_portal(next_position, world):
                    if dimension == 0:
                        continue
                    next_dimension -= 1
                else:
                    next_dimension += 1

                next_position = teleport_position[next_position]

            queue.append((next_position, next_distance, next_dimension))
            visited.add((next_dimension, next_position))
