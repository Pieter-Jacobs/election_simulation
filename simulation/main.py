from imports import *
from classes.Election import Election
from classes.Plotter import Plotter
import numpy as np

SEED = 2021

@hydra.main(config_path="conf", config_name="config.yaml")
def main(cfg: DictConfig):
    np.random.seed(SEED)
    election = Election(cfg)
    election.count_votes()
    Plotter(election)


if __name__ == "__main__":
    main()
