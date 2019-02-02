import dataclasses
import re
from glob import glob
from typing import Dict, List, Union
from pprint import pprint

from src import operators
from src.config import Config
from src.models import Individual, Population, PopulationStr, stringify_population

# -------------------------------------------------------
# Fitness analysis
# -------------------------------------------------------

# TODO: somehow precompute fitness for every individual. Most analyses use it.


def total_fitness(pop: Population) -> int:
    return sum(operators.fitness(ind) for ind in pop)


def avg_fitness(pop: Population) -> int:
    return total_fitness(pop) / len(pop)


def max_fitness(pop: Population) -> int:
    return max(operators.fitness(ind) for ind in pop)


# -------------------------------------------------------
# Per-generation breakdown
# -------------------------------------------------------


def gens_to_population(generations: List[Population]) -> Dict[int, PopulationStr]:
    return {i: stringify_population(pop) for i, pop in enumerate(generations)}


def gens_to_max_fitness(generations: List[Population]) -> Dict[int, int]:
    return {i: max_fitness(pop) for i, pop in enumerate(generations)}


def gens_to_avg_fitness(generations: List[Population]) -> Dict[int, int]:
    return {i: avg_fitness(pop) for i, pop in enumerate(generations)}


def gens_to_complete_analysis(generations: List[Population]) -> Dict[int, int]:
    return {
        i: {
            "total_fitness": total_fitness(pop),
            "avg_fitness": avg_fitness(pop),
            "max_fitness": max_fitness(pop),
            "population": stringify_population(pop),
        }
        for i, pop in enumerate(generations)
    }


# -------------------------------------------------------
# Aggregate analysis
# -------------------------------------------------------


def aggregate(generations: List[Population]) -> Dict[str, Union[str, int, float]]:
    total_avg_fitness = sum(total_fitness(pop) for pop in generations) / (
        len(generations) * len(generations[0])
    )
    total_max_fitness = max(max_fitness(pop) for pop in generations)
    return {
        "total_avg_fitness": total_avg_fitness,
        "total_max_fitness": total_max_fitness,
        "first_gen_max_fitness_met": next(
            i
            for i, pop in enumerate(generations)
            if max_fitness(pop) >= total_max_fitness
        ),
        "first_gen_total_avg_fitness_met": next(
            i
            for i, pop in enumerate(generations)
            if avg_fitness(pop) >= total_avg_fitness
        ),
    }


# -------------------------------------------------------
# Save to file
# -------------------------------------------------------


def write_analysis(generations: List[Population], config: Config, path: str) -> None:
    output = {
        "config": dataclasses.asdict(config),
        "aggregrate_analysis": aggregate(generations),
        "result": gens_to_complete_analysis(generations),
    }
    with open(path, "w") as f:
        pprint(output, stream=f, width=100, compact=True)


def generate_file_name(dir_path: str) -> str:
    current_files = glob(f"{dir_path}/run*.txt")
    max_num = max(int(re.findall(r"\d{3}", f)[0]) for f in current_files)
    return f"{dir_path}/run{max_num + 1:03d}.txt"


# -------------------------------------------------------
# Graphs
# -------------------------------------------------------
