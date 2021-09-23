from imports import *
from classes.Voter import Voter
import numpy as np


class Election:
    """ 
    Defines a class that is used to run a simulation of a democratic election

    Attributes:
    -----------
    polls: list of int
        Dispatcher used to dispatch the choice of query function
    parties: list of list of
        The language model used for classification
    voters: list of Voter
        String representing the chosen query function

    Methods
    -------
    count_votes():
        Counts the votes for each party and determines the amount of strategic votes
    init_parties():
        Initialises the parties based hard coded vectors in a text file
    init_voters():
        Initialises voters based on the polls
    """
    def __init__(self, cfg) -> None:
        """
        Parameters:
        -----------
        cfg: DictConfig 
            Dictionary containing the configuration of the hyperparameters
        """
        self.polls = np.array(cfg.polls.distribution) * cfg.polls.voters
        self.parties = self.init_parties()
        self.voters = self.init_voters()
        pass

    def count_votes(self):
        """Counts and prints the votes for each party and the percentage of strategic votes"""
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
        vote_percentages = {k: v / len(self.voters) for k, v in vote_count.items()}
        print("Percentage of votes gathered by each party:")
        print(vote_percentages)
        print("Percentage of strategic votes:")
        print(strategic_vote_count / len(self.voters))

    def init_parties(self):
        """Initialises the parties based hard coded vectors in a text file"""
        parties = np.genfromtxt(hydra.utils.get_original_cwd(
        ) + os.path.sep + 'party_vector.csv', delimiter=',')
        return parties

    def init_voters(self):
        """Initialises voters based on the polls"""
        voters = [Voter(i, self.parties) for i in range(len(self.polls)) for j in range(int(self.polls[i]))]
        return voters
