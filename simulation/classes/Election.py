from imports import *
from classes.Voter import Voter
import numpy as np


class Election:
    def __init__(self, cfg) -> None:
        self.polls = np.array(cfg.polls.distribution) * cfg.polls.voters
        self.parties = self.init_parties()
        self.voters = self.init_voters()
        pass

    def count_votes(self):
        print("Counting votes...")
        vote_count = {}
        strategic_vote_count = 0
        for voter in self.voters:
            vote, strategic = voter.vote(self.polls)
            if strategic:
                strategic_vote_count += 1
            if vote not in vote_count.keys():
                vote_count[vote] = 0 
            else:
                vote_count[vote] += 1
        print(vote_count)
        vote_percentages = {k: v / len(self.voters) for k, v in vote_count.items()}

        print(vote_percentages)
        print(strategic_vote_count)


    def init_parties(self):
        parties = np.genfromtxt(hydra.utils.get_original_cwd(
        ) + os.path.sep + 'party_vector.csv', delimiter=',')
        return parties

    def init_voters(self):
        voters = [Voter(i, self.parties) for i in range(len(self.polls)) for j in range(int(self.polls[i]))]
        return voters
