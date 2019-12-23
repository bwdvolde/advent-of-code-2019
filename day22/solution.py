import re

from read_file.read_file import read_file

techniques = """deal into new stack
cut -2
deal with increment 7
cut 8
cut -4
deal with increment 7
cut 3
deal with increment 9
deal with increment 3
cut -1""".split("\n")

techniques = read_file("input.txt")[:-1]

deck_size = 10007
deck = list(range(deck_size))


def perform_increment(deck, n):
    new_deck = [0] * len(deck)
    for i in range(len(deck)):
        new_i = i * n % len(deck)
        new_deck[new_i] = deck[i]
    return new_deck


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


for technique in techniques:
    if technique == "deal into new stack":
        deck = deck[::-1]

    cut_match = re.match("cut (.*)", technique)
    if cut_match:
        cut_size = int(cut_match.group(1))
        deck = deck[cut_size:] + deck[:cut_size]

    increment_match = re.match("deal with increment (.*)", technique)
    if increment_match:
        n = int(increment_match.group(1))
        deck = perform_increment(deck, n)


print(deck)
print(deck.index(2019))

