import functools
import random
from typing import List

from tqdm import tqdm

from src.models import Individual, Population
from src import operators


def generation(
    pop: Population, *, tournament_size: int, p_crossover: float, p_mutation: float
) -> Population:
    selected = operators.tournament(pop, k=tournament_size)
    crossed: Population = []
    while len(crossed) < len(selected):
        ran1, ran2 = random.choices(selected, k=2)
        new1, new2 = operators.crossover(ran1, ran2, p=p_crossover)
        crossed.append(new1)
        crossed.append(new2)
    # ensure crossover is same size
    if len(crossed) > len(selected):
        ran_ind = random.choice(crossed)
        crossed.remove(ran_ind)
    return [operators.mutate(ind, p=p_mutation) for ind in crossed]


def run_ga(
    *,
    num_generations: int,
    num_ind: int,
    num_genes: int,
    tournament_size: int,
    p_crossover: float,
    p_mutation: float
) -> List[Population]:
    initial_pop = operators.gen_population(num_ind=num_ind, num_genes=num_genes)
    curr_pop = initial_pop
    hist: List[Population] = [initial_pop]
    compute_generation = functools.partial(
        generation,
        tournament_size=tournament_size,
        p_crossover=p_crossover,
        p_mutation=p_mutation,
    )
    print(f"Running genetic algorithm for {num_generations} generations!\n")
    for _ in tqdm(range(num_generations)):
        new_pop = compute_generation(curr_pop)
        hist.append(new_pop)
        curr_pop = new_pop
    print()
    return hist
