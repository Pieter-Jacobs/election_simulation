from imports import *
from classes.Election import Election
import numpy as np

@hydra.main(config_path="conf", config_name="config.yaml")
def main(cfg: DictConfig):
    election = Election(cfg)
    election.count_votes()
    pass



if __name__ == "__main__":
    main()
