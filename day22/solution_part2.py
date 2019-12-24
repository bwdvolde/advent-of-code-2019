import itertools
import re

from read_file.read_file import read_file

# techniques = """deal into new stack
# cut -2
# deal with increment 7
# cut 8
# cut -4
# deal with increment 7
# cut 3
# deal with increment 9
# deal with increment 3
# cut -1""".split("\n")


techniques = read_file("input.txt")[:-1]


def egcd(a, b):
    if a == 0:
        return (b, 0, 1)
    else:
        g, y, x = egcd(b % a, a)
        return (g, x - (b // a) * y, y)


def modinv(a, m):
    g, x, y = egcd(a, m)
    if g != 1:
        raise Exception('modular inverse does not exist')
    else:
        return x % m


def find_powers_of_two(number):
    result = []
    current_power = 1
    while number:
        if number % 2:
            result.append(current_power)
        number //= 2
        current_power *= 2
    return result


def find_element_at_index(i, deck_size, techniques):
    if not techniques:
        return i

    previous_i = i
    last_technique = techniques.pop()

    if last_technique == "deal into new stack":
        previous_i = (-i - 1)

    cut_match = re.match("cut (.*)", last_technique)
    if cut_match:
        c = int(cut_match.group(1))
        previous_i = i + c

    increment_match = re.match("deal with increment (.*)", last_technique)
    if increment_match:
        n = int(increment_match.group(1))
        n_inv = modinv(n, deck_size)
        previous_i = i * n_inv

    previous_i %= deck_size
    return find_element_at_index(previous_i, deck_size, techniques)


def rewrite_techniques(techniques, deck_size):
    techniques = techniques[:]

    current_cut = 0
    current_increment = 1
    for technique in techniques:

        if technique == "deal into new stack":
            current_increment *= (deck_size - 1)
            current_cut = -current_cut + 1

        cut_match = re.match("cut (.*)", technique)
        if cut_match:
            cut_match = int(cut_match.group(1))
            current_cut += cut_match
        increment_match = re.match("deal with increment (.*)", technique)
        if increment_match:
            increment_match = int(increment_match.group(1))
            current_cut *= increment_match
            current_increment *= increment_match

        current_cut %= deck_size
        current_increment %= deck_size
    return ["deal with increment {}".format(current_increment), "cut {}".format(current_cut)]


deck_size = 119315717514047
apply_n_times = 101741582076661

techniques = rewrite_techniques(techniques, deck_size)

techniques_for_power = {1: techniques}
current = 2
while current < apply_n_times:
    techniques_previous_power = techniques_for_power[current // 2]
    techniques_current_power = rewrite_techniques(techniques_previous_power * 2, deck_size)
    techniques_for_power[current] = techniques_current_power
    current *= 2

powers_of_two = find_powers_of_two(apply_n_times)
final_techniques = [techniques_for_power[power] for power in powers_of_two]
final_techniques = list(itertools.chain(*final_techniques))
final_techniques = rewrite_techniques(final_techniques, deck_size)

print("Part 2:", find_element_at_index(2020, deck_size, final_techniques[:]))
