import os
import hydra
import matplotlib

from classes.Election import Election
from classes.Voter import Voter

class Plotter:
  def __init__(self, election: Election) -> None:
    matrix = Voter.switch_matrix()
    swing = election.swing
    cfg = election.cfg
    print(os.getcwd())
    filename = hydra.utils.get_original_cwd() + os.sep + cfg.polls.name + "_unc_" + str(cfg.uncertainty) + "_swing_" + str(cfg.swing)

    with open(filename + "conf_matrix.csv", "w") as f:
      f.write(matrix)
      f.close()

    

