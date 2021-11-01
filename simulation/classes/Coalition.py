import numpy as np
from numpy.lib.function_base import average
from helpers import *


class Coalition:
    party_vectors = None    # Static variable containing all opinions of all participating parties

    """Constructor. Set static Coalition.party_vectors before calling
        Parameters:
        -----------
        parties: numpy.ndarray 
            The indices participating parties in Coalition.party_vectors
        polls: numpy.ndarray 
            The amount of votes expected for each party, same order as the parties parameter
    """
    def __init__(self, parties: np.ndarray, polls: np.ndarray):
        self.parties = parties
        self.polls = polls
        self.feasibility = self.coalition_feasibility(parties)
        self.profile = self.coalition_profile()


    """Returns the profile of the coalition. Weighted average on all opinions
       of all parties in the coalition. Weights defined by distribution of seats
    """
    def coalition_profile(self) -> np.ndarray:
        # Dimensionality of the opinion vector space
        vector_length = Coalition.party_vectors[0].shape[0]

        # For each issue take weighted average of coalition opinions
        profile = [np.average([Coalition.party_vectors[party][idx] for party in self.parties], weights = self.polls) for idx in range(vector_length)]
        return np.asarray(profile)


    """
    Returns the feasibility of the Coalition, dependent on the similarity of their views.
    Takes an unweighted average of the cosine similarities between all parties in the coalition.
    """
    def coalition_feasibility(self, parties: list) -> float:
        return average([cosine_similarity(Coalition.party_vectors[j], Coalition.party_vectors[i]) for idx, i in enumerate(parties[:-1])\
                                                                                                  for j      in parties[idx+1:]])


    """
    String representation of Coalition class
    """
    def __str__(self) -> str:
        return str(self.parties) + "\t" + str(self.feasibility)



      """Find all possible coalitions

      Returns:
          [[int]]: list of coalitions. Coalition is list of participating parties
      """
    @staticmethod
    def __find_permutations(polls, cur_parties = [], cur_idx = 0) -> list:
        # Base case: cur_parties can form coalition immediately
        if sum([(polls[cur_party]) for cur_party in cur_parties]) >= 0.5:
            return [cur_parties]
        # Base Case: cur_parties can never form coalition
        if len(cur_parties) >= 5 or cur_idx == len(Coalition.party_vectors): 
            return []

        # 
        coalitions = Coalition.init_coalitions(polls, cur_parties, cur_idx + 1) + \
                     Coalition.init_coalitions(polls, cur_parties + [cur_idx], cur_idx + 1)

        return coalitions

    @staticmethod
    def init_coalitions(party_vectors, polls):
        Coalition.party_vectors = party_vectors

        new_coalitions = []
        for coalition in Coalition.__find_permutations(polls):
            coal_polls = [polls[party] for party in coalition]
            if sum(coal_polls) - min(coal_polls) <= 0.5:
                new_coalitions += [Coalition(coalition, coal_polls)]

        new_coalitions.sort(key=lambda x:x.feasibility, reverse=True)
        return new_coalitions

