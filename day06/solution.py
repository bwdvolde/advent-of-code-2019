from collections import defaultdict


def read_file(path):
    with open(path, "r") as file:
        file_content = file.read()
        lines = file_content.splitlines()
        return lines


def compute_total_orbits(children_of):
    total_orbits = 0

    stack = [("COM", 0)]
    while stack:
        node, depth = stack.pop()
        depth += 1
        for child in children_of[node]:
            total_orbits += depth
            stack.append((child, depth))

    return total_orbits


def compute_children_parents(orbit_strings):
    children_of = defaultdict(list)
    parent_of = {}
    for string in orbit_strings:
        parent, child = string.split(")")
        children_of[parent].append(child)
        parent_of[child] = parent
    return children_of, parent_of


def compute_transfers_needed(parent_of):
    def compute_parents(node):
        parents = []
        while parent_of.get(node):
            node = parent_of[node]
            parents.append(node)
        return parents[::-1]

    parents_you = compute_parents("YOU")
    parents_san = compute_parents("SAN")

    depth_you = len(parents_you)
    depth_san = len(parents_san)

    i = 0
    while parents_you[i] == parents_san[i]:
        i += 1
    depth_lca = i - 1

    return (depth_you - depth_lca) + (depth_san - depth_lca) - 2


if __name__ == "__main__":
    orbit_strings = read_file("input.txt")
    children_of, parent_of = compute_children_parents(orbit_strings)

    print("Part 1", compute_total_orbits(children_of))
    print("Part 2,", compute_transfers_needed(parent_of))
