import configparser
from dataclasses import dataclass


@dataclass(frozen=True)
class Config:
    seed: int
    num_genes: int
    num_individuals: int
    num_generations: int
    p_mutation: float
    p_crossover: float
    tournament_size: int


def read(path: str) -> Config:
    cp = configparser.ConfigParser()
    cp.read(path)
    return Config(
        seed=int(cp["environment"]["seed"]),
        num_genes=int(cp["size"]["num_genes"]),
        num_individuals=int(cp["size"]["num_individuals"]),
        num_generations=int(cp["size"]["num_generations"]),
        p_mutation=float(cp["mutation"]["p"]),
        p_crossover=float(cp["crossover"]["p"]),
        tournament_size=int(cp["selection"]["k"]),
    )
