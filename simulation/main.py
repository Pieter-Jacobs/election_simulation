from imports import *
from classes.Election import Election
import numpy as np

@hydra.main(config_path="conf", config_name="config.yaml")
def main(cfg: DictConfig):
    #polls = np.array(cfg.polls.distribution) * cfg.polls.voters
    election = Election()
    pass



if __name__ == "__main__":
    main()
