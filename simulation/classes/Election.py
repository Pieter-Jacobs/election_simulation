from imports import *
from classes.Voter import Voter
import numpy as np


class Election:
    def __init__(self, cfg) -> None:
        self.polls = np.array(cfg.polls.distribution) * cfg.polls.voters
        self.parties = self.init_parties()
        self.voters = self.init_voters()
        self.voters[100].vote(self.polls)
        pass

    def init_parties(self):
        parties = np.genfromtxt(hydra.utils.get_original_cwd(
        ) + os.path.sep + 'party_vector.csv', delimiter=',')
        return parties

    def init_voters(self):
        voters = [Voter(i, self.parties) for i in range(len(self.parties)) for j in range(len(self.parties[i]))]
        return voters
