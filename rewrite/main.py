from imports import *
from plot import *
from serialize import *
from classes.Election import Election
import numpy as np


@hydra.main(config_path="conf", config_name="config.yaml")
def main(cfg: DictConfig):
    for run in range(cfg.n_runs):
        np.random.seed(run)
        election = Election(n_seats=cfg.n_seats,
                            n_voters=cfg.n_voters, polls=cfg.polls.distribution, upper_swing=cfg.upper_swing)
        results, vote_matrix, percentage_strategic = election.start()
        write_string_to_file(string=f"{results}", path=hydra.utils.get_original_cwd() + os.sep + "data" + os.sep
                             + "election_results" + os.sep + cfg.polls.name + "_swing_" + str(cfg.upper_swing) + "_run_" + str(run))
        write_string_to_file(string=f"{percentage_strategic}", path=hydra.utils.get_original_cwd() + os.sep + "data" + os.sep
                             + "strategic_voting_stats" + os.sep + cfg.polls.name + "_swing_" + str(cfg.upper_swing) + "_run_" + str(run))
        write_matrix_to_file(matrix=vote_matrix, path=hydra.utils.get_original_cwd(
        ) + os.sep + "data" + os.sep + "voter_matrices" + os.sep + cfg.polls.name + "_swing_" + str(cfg.upper_swing) + "_run_" + str(run))


if __name__ == "__main__":
    main()
