from imports import *
from helpers import cosine_similarity
import numpy as np


class Coalition(object):
    def __init__(self, parties: list) -> None:
        """
        Represents a coalition consisting of parties

        Parameters:
        -----------
        parties: list 
            The mappings of participating parties
        polls: list
            The amount of votes expected for each party
        """
        self.parties = parties
        self.polls = [party.polled_votes for party in parties]
        self.feasibility = self.coalition_feasibility()
        self.profile = self.coalition_profile()
        super().__init__()

    def __str__(self) -> str:
        parties = "["
        for party in self.parties:
            parties += str(party) + ", "
        parties = parties[:-2] + "]"
        return parties + '\t' + str(self.feasibility)

    def coalition_feasibility(self) -> float:
        """
        Returns the feasibility of the Coalition, dependent on the similarity of their views.
        Takes an unweighted average of the cosine similarities between all parties in the coalition.
        """
        return average([cosine_similarity(party_1.profile, party_2.profile) for idx, party_1 in enumerate(self.parties[:-1])
                        for party_2 in self.parties[idx+1:]])

    def coalition_profile(self) -> list:
        """
        Returns the profile of the coalition. Weighted average on all opinions
        of all parties in the coalition. Weights defined by distribution of seats
        """
        # Dimensionality of the opinion vector space
        vector_length = self.parties[0].profile.shape[0]
        # For each issue take weighted average of coalition opinions
        profile = [np.average([party.profile[idx] for party in self.parties],
                              weights=self.polls) for idx in range(vector_length)]
        return profile
