import random
from typing import List

from src.models import Individual, Population


# --------------------------------------------------------
# Initialize data
# --------------------------------------------------------


def gen_individual(num_genes: int) -> Individual:
    return [random.choice([False, True]) for _ in range(num_genes)]


def gen_population(*, num_ind: int, num_genes: int) -> Population:
    return [gen_individual(num_genes) for _ in range(num_ind)]


# --------------------------------------------------------
# Fitness
# --------------------------------------------------------


def fitness(ind: Individual) -> int:
    return sum(ind) / len(ind)


# --------------------------------------------------------
# Mutation
# --------------------------------------------------------


def mutate(ind: Individual, *, p: float) -> Individual:
    return [not b if random.random() < p else b for b in ind]


# --------------------------------------------------------
# Crossover
# --------------------------------------------------------


def crossover(
    ind1: Individual, ind2: Individual, *, p: float
) -> (Individual, Individual):
    if random.random() >= p:
        return (ind1, ind2)
    cross_point = random.randrange(1, len(ind1))
    return (
        ind1[:cross_point] + ind2[cross_point:],
        ind2[:cross_point] + ind1[cross_point:],
    )


# --------------------------------------------------------
# Selection
# --------------------------------------------------------


def compete(inds: List[Individual]) -> Individual:
    # Note an alternative implementation is to sort by fitness then give each the
    # probability w_n = p*((1-p)^(n-1)) to win, with n startinag at 0."""
    return max(inds, key=fitness)


def tournament(pop: Population, *, k: int) -> Population:
    new_pop: Population = []
    while len(new_pop) < len(pop):
        pool = random.choices(pop, k=k)
        winner = compete(pool)
        new_pop.append(winner)
    return new_pop
