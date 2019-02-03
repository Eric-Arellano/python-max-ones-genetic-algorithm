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
    analysis.write_analysis(result, conf, analysis.generate_run_file_name("output"))
    analysis.graph(result, analysis.generate_graph_file_name("output"))
