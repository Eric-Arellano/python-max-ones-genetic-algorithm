import random

from src import analysis, config, pipeline

if __name__ == "__main__":
    conf = config.read("resources/config.ini")
    random.seed(conf.seed)
    result = pipeline.run_ga(
        num_generations=conf.num_generations,
        num_ind=conf.num_individuals,
        num_genes=conf.num_genes,
        tournament_size=conf.tournament_size,
        p_crossover=conf.p_crossover,
        p_mutation=conf.p_mutation,
    )
    print(analysis.output_generations(result))