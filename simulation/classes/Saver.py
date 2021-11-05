import os
import hydra

from classes.Election import Election
from classes.Voter import Voter


class Saver:
  def __init__(self, election: Election) -> None:
    cfg = election.cfg
    to_write = f"{election.cfg.swing} {election.strategic_vote_count}\n"
    to_write += f"votes: {election.vote_percentages}\n"
    to_write += f"seats: {election.seats}\n"
    to_write += Voter.switch_matrix()
    filename = hydra.utils.get_original_cwd() + os.sep + "saver" + os.sep + cfg.polls.name + "_unc_" + str(cfg.uncertainty) + "_swing_" + str(cfg.swing) + "_run_" + str(cfg.run)
    with open(filename, "w") as f:
      f.write(to_write)
      f.close()
    