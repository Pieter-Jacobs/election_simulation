from imports import *


@hydra.main(config_path="conf", config_name="config.yaml")
def main(cfg: DictConfig):
    print(cfg.polls)
    pass



if __name__ == "__main__":
    main()
