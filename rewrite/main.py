from imports import *
from classes.Election import Election
import numpy as np


@hydra.main(config_path="conf", config_name="config.yaml")
def main(cfg: DictConfig):
    np.random.seed(cfg.seed)
    election = Election(n_seats=cfg.n_seats,
                        n_voters=cfg.n_voters, polls=cfg.polls.distribution, max_swing=cfg.max_swing)

if __name__ == "__main__":
    main()
