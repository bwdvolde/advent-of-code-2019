import itertools

import numpy as np


class Moon:

    def __init__(self, position):
        self.position = np.array(position)
        self.velocity = np.zeros(3, dtype=int)

    def step(self):
        self.position += self.velocity

    def total_energy(self):
        potential_enery = np.sum(np.abs(self.position))
        kinetic_engery = np.sum(np.abs(self.velocity))
        return potential_enery * kinetic_engery

    def __repr__(self):
        return "pos=" + str(self.position) + " vel=" + str(self.velocity)


def update_velocities(moons):
    combinations = itertools.combinations(moons, 2)
    for combination in combinations:
        moon_a, moon_b = combination
        d_velocity_a = np.where(moon_a.position < moon_b.position, 1, -1)
        d_velocity_a[moon_a.position == moon_b.position] = 0
        d_velocity_b = - d_velocity_a

        moon_a.velocity += d_velocity_a
        moon_b.velocity += d_velocity_b


initial_positions = np.array([
    [12, 0, -15],
    [-8, -5, -10],
    [7, -17, 1],
    [2, -11, -6]
])


def init_moons():
    return [Moon(position) for position in initial_positions]


def simulate(n_steps=10 ** 1000, early_stop_dimension=None):
    moons = init_moons()
    for step in range(n_steps):
        update_velocities(moons)

        for moon in moons:
            moon.step()

        if early_stop_dimension is not None:
            if all([moon.velocity[early_stop_dimension] == 0 for moon in moons]):
                return moons, 2 * (step + 1)

    return moons, n_steps


moons, _ = simulate(n_steps=1000)
total_energy = sum([moon.total_energy() for moon in moons])
print("Part 1:", total_energy)

steps_needed_dimension = []
for dimension in [0, 1, 2]:
    _, steps_needed = simulate(early_stop_dimension=dimension)
    steps_needed_dimension.append(steps_needed)

# object dtype because we need big numbers
steps_needed_dimension = np.array(steps_needed_dimension, dtype=object)
steps_needed = np.lcm.reduce(steps_needed_dimension)
print("Part 2:", steps_needed)
