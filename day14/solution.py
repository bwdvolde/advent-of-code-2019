import math
from collections import defaultdict

from read_file.read_file import read_file


class ChemicalWithQuantity:

    def __init__(self, quantity, chemical):
        self.quantity = quantity
        self.chemical = chemical

    @staticmethod
    def from_string(string):
        string = string.strip()
        quantity, chemical = string.split(" ")
        quantity = int(quantity)
        return ChemicalWithQuantity(quantity, chemical)

    def __repr__(self) -> str:
        return "{} {}".format(self.quantity, self.chemical)


class Reaction:

    def __init__(self, reagents, result):
        self.reagents = reagents
        self.result = result

    def __repr__(self):
        return "{} => {}".format(self.reagents, self.result)


def build_reactions(lines):
    reactions = []
    for line in lines:
        if not line:
            continue
        input_string, result_string = line.split("=>")
        reagent_strings = input_string.split(",")

        reagents = [ChemicalWithQuantity.from_string(string) for string in reagent_strings]
        result = ChemicalWithQuantity.from_string(result_string)

        reaction = Reaction(reagents, result)
        reactions.append(reaction)
    return reactions


lines = read_file("input.txt")

reactions = build_reactions(lines)
reaction_of = {reaction.result.chemical: reaction for reaction in reactions}


def calculate_reagents(chemical, quantity_needed):
    if chemical == "ORE":
        return {chemical: quantity_needed}

    reaction = reaction_of[chemical]
    result = reaction.result
    reagents = reaction.reagents

    reactions_needed = math.ceil(quantity_needed / result.quantity)
    reduction = {reagent.chemical: reagent.quantity * reactions_needed for reagent in reagents}

    # Add leftover chemicals as negative quantity in reduction
    leftover_chemicals = (reactions_needed * result.quantity) - quantity_needed
    if leftover_chemicals:
        reduction[chemical] = -leftover_chemicals

    return reduction


def is_final_reaction(reaction):
    return all(chemical == "ORE" or quantity < 0 for chemical, quantity in reaction.items())


def reduce_reaction(reaction):
    reduced_reaction = defaultdict(lambda: 0)

    for chemical, quantity_needed in reaction.items():
        reagents = calculate_reagents(chemical, quantity_needed)

        for chemical, quantity in reagents.items():
            if quantity:
                reduced_reaction[chemical] += quantity

    return reduced_reaction


def find_final_reaction(current_reaction):
    while not is_final_reaction(current_reaction):
        current_reaction = reduce_reaction(current_reaction)
    return current_reaction


def calculate_ore_needed(fuel):
    return find_final_reaction({"FUEL": fuel})["ORE"]


ore = calculate_ore_needed(1)
print("Part 1:", ore)

fuel_min = 1
fuel_max = ore
while fuel_min < fuel_max:
    fuel_mid = (fuel_min + fuel_max) // 2
    ore_needed = calculate_ore_needed(fuel_mid)

    if ore_needed > 10 ** 12:
        fuel_max = fuel_mid - 1
    else:
        fuel_min = fuel_mid

print("Part 2:", fuel_min)
