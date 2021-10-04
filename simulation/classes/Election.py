from imports import *
from classes.Voter import Voter
import numpy as np
import statistics as stat


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
        self.voters = self.init_voters(cfg.swing)
        self.calculate_chance_to_influence()

    def count_votes(self):
        """Counts and prints the votes for each party and the percentage of strategic votes"""
        print("Counting votes...")
        vote_count = {}
        strategic_vote_count = 0
        for voter in self.voters:
            vote, strategic = voter.vote(self.chances)
            strategic_vote_count += strategic
            if vote not in vote_count.keys():
                vote_count[vote] = 0 
            else:
                vote_count[vote] += 1
        vote_percentages = {k: str(v / len(self.voters) * 100) + "%" for k, v in vote_count.items()}
        print("Percentage of votes gathered by each party:")
        print(vote_percentages)
        print("Percentage of strategic votes:")
        print(str((strategic_vote_count / len(self.voters)) * 100) + '%')

    def init_parties(self):
        """Initialises the parties based hard coded vectors in a text file"""
        parties = np.genfromtxt(hydra.utils.get_original_cwd(
        ) + os.path.sep + 'party_vector.csv', delimiter=',')
        return parties

    def init_voters(self, max_swing):
        """Initialises voters based on the polls"""
        voters = [Voter(i, self.parties, max_swing) for i in range(len(self.polls)) for j in range(int(self.polls[i]))]
        return voters
        

    def calculate_chance_to_influence(self):
        """ 
            Returns the expectation a vote to make a difference, based upon the parties poll rankings. 
            Currently based on winner takes all
        """
        
        poll_uncertainty = 0.25   # Parameter indicating uncertainty in the poll / Maybe put in config

        most_votes = np.max(self.polls)
        self.chances = np.zeros(30)

        for idx, poll_result in enumerate(np.nditer(self.polls)):
          sigma = poll_result * poll_uncertainty
          if sigma == 0:
            sigma = 0.001

          dist = stat.NormalDist(poll_result, sigma)
          self.chances[idx] = 1 - dist.cdf(most_votes)

        print(self.chances)

