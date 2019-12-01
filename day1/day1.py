def read_file(path):
    with open(path, "r") as file:
        file_content = file.read()
        lines = file_content.splitlines()
        return list(map(int, lines))


def compute_fuel(mass):
    """
    >>> compute_fuel(14)
    2
    >>> compute_fuel(100756)
    33583
    """
    return max(0, mass // 3 - 2)


def compute_fuel_part_2(mass):
    """
    >>> compute_fuel_part_2(1969)
    966
    >>> compute_fuel_part_2(100756)
    50346
    """
    total_fuel = 0
    fuel = compute_fuel(mass)
    while fuel > 0:
        total_fuel += fuel
        fuel = compute_fuel(fuel)

    return total_fuel


if __name__ == "__main__":
    import doctest
    doctest.testmod()

    masses = read_file("input.txt")

    total_mass = sum(compute_fuel(mass) for mass in masses)
    print("Part 1:", total_mass)

    total_mass = sum(compute_fuel_part_2(mass) for mass in masses)
    print("Part 2:", total_mass)
