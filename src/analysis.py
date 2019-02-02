from typing import Dict, List

from src.models import Individual, Population, PopulationStr, stringify_population


def output_generations(result: List[Population]) -> Dict[int, PopulationStr]:
    return {i: stringify_population(pop) for i, pop in enumerate(result)}
