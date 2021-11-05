from imports import *
from classes.Election import Election
from classes.Saver import Saver
import numpy as np

@hydra.main(config_path="conf", config_name="config.yaml")
def main(cfg: DictConfig):
    np.random.seed(cfg.run)
    election = Election(cfg)
    election.count_votes()
    Saver(election)


if __name__ == "__main__":
    main()
