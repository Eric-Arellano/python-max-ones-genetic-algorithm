from typing import List

Bit = bool
Individual = List[Bit]
Population = List[Individual]

BitChar = str
IndividualStr = str
PopulationStr = List[IndividualStr]


def normalize_bitchar(c: BitChar) -> Bit:
    return c == "1"


def normalize_individualstr(ind: IndividualStr) -> Individual:
    return [normalize_bitchar(c) for c in ind]


def normalize_populationstr(ps: PopulationStr) -> Population:
    return [normalize_individualstr(ind) for ind in ps]


def stringify_bit(bit: Bit) -> BitChar:
    return "1" if bit else "0"


def stringify_individual(ind: Individual) -> IndividualStr:
    return "".join(stringify_bit(b) for b in ind)


def stringify_population(pop: Population) -> PopulationStr:
    return [stringify_individual(ind) for ind in pop]
