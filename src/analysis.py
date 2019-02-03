import dataclasses
import re
from glob import glob
from typing import Dict, List, Union
from pprint import pprint

from src import operators
from src.config import Config
from src.models import Individual, Population, PopulationStr, stringify_population

import matplotlib

matplotlib.use("TkAgg")
from matplotlib import pyplot

# -------------------------------------------------------
# Fitness analysis
# -------------------------------------------------------


def total_fitness(pop: Population) -> float:
    return sum(operators.fitness(ind) for ind in pop)


def avg_fitness(pop: Population) -> float:
    return total_fitness(pop) / len(pop)


def max_fitness(pop: Population) -> float:
    return max(operators.fitness(ind) for ind in pop)


# -------------------------------------------------------
# Per-generation breakdown
# -------------------------------------------------------


def gens_to_population(generations: List[Population]) -> Dict[int, PopulationStr]:
    return {i: stringify_population(pop) for i, pop in enumerate(generations)}


def gens_to_max_fitness(generations: List[Population]) -> Dict[int, float]:
    return {i: max_fitness(pop) for i, pop in enumerate(generations)}


def gens_to_avg_fitness(generations: List[Population]) -> Dict[int, float]:
    return {i: avg_fitness(pop) for i, pop in enumerate(generations)}


def gens_to_complete_analysis(
    generations: List[Population]
) -> Dict[int, Dict[str, Union[float, List[str]]]]:
    return {
        i: {
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
    num_generations = len(generations)
    total_avg_fitness = sum(total_fitness(pop) for pop in generations) / (
        num_generations * len(generations[0])
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
        "ratio_gens_max_fitness_met": sum(
            1 for pop in generations if max_fitness(pop) >= total_max_fitness
        )
        / num_generations,
        "ratio_gens_avg_fitness_met": sum(
            1 for pop in generations if avg_fitness(pop) >= total_avg_fitness
        )
        / num_generations,
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


def _generate_file_name(dir_path: str, prefix: str, extension: str) -> str:
    current_files = glob(f"{dir_path}/{prefix}*.{extension}")
    nums = {int(re.findall(r"\d{3}", f)[0]) for f in current_files} | {-1}
    return f"{dir_path}/{prefix}{max(nums) + 1:03d}.{extension}"


def generate_run_file_name(dir_path: str) -> str:
    return _generate_file_name(dir_path, "run", "txt")


# -------------------------------------------------------
# Graphs
# -------------------------------------------------------


def graph(generations: List[Population], path: str) -> None:
    max_fitness_data = gens_to_max_fitness(generations)
    avg_fitness_data = gens_to_avg_fitness(generations)
    open_circle_dotted_line = "o:"
    pyplot.plot(
        max_fitness_data.values(), f"b{open_circle_dotted_line}", label="max_fitness"
    )
    pyplot.plot(
        avg_fitness_data.values(), f"g{open_circle_dotted_line}", label="avg_fitness"
    )
    pyplot.xlabel("Generation")
    pyplot.ylabel("Fitness")
    pyplot.title("Genetic algorithm performance")
    pyplot.legend()
    pyplot.savefig(path)


def generate_graph_file_name(dir_path: str) -> str:
    return _generate_file_name(dir_path, "graph", "png")
