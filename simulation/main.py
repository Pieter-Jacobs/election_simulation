from imports import *
import numpy as np

@hydra.main(config_path="conf", config_name="config.yaml")
def main(cfg: DictConfig):
    polls = np.array(cfg.polls.distribution) * cfg.polls.voters
    print(polls)
    pass



if __name__ == "__main__":
    main()
