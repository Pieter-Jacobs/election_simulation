from imports import *
from helpers import cosine_similarity
import numpy as np
from classes.Party import Party
from classes.Coalition import Coalition


class Voter(object):
    """A class representing a voter.

    Attributes:
        swing (float): The swing of the voter.
        profile: The political preference
        similarities: The similarities of the voter to each party
        party: The party the voter is initially voting for
        expected_party_seats: The expected number of seats the party will get
    """
    def __init__(self, initial_party: Party, parties: list, upper_swing: float) -> None:
        self.swing = np.random.uniform(low=0, high=upper_swing)
        self.profile = self.create_position(initial_party)
        self.similarities = self.compute_similarities(parties)
        self.party = parties[np.argmax(self.similarities)]
        self.expected_party_seats = 0
        super().__init__()


    """
    Lets the candidate vote based on the voter's profile, the candidate's profile
    and strategic reasons.
      parties: The list of candidate parties
      coalitions: The list of possible coalitions according to poll
      residual_seats: The list of seats % 1 for each party
    """
    def vote(self, parties: list, coalitions: list, residual_seats: list) -> Party:
        scores = self.similarities + residual_seats + \
            self.compute_coalition_scores(parties, coalitions)
        party = parties[np.argmax(scores)]
        self.voted_for = party
        self.expected_party_seats = party.polled_votes
        return party


    """
    Compute the similarity of the voter to each party

    Args:
        parties: The list of candidate parties
    """
    def compute_similarities(self, parties: list) -> list:
        similarities = np.array([cosine_similarity(
            self.profile, parties[i].profile) for i in range(len(parties))])
        return similarities
    

    """
    Returns if voter voted strategically
    """
    def voted_strategic(self) -> bool:
        return self.voted_for != self.party


    """
    Find voter happiness with election outcome

    Returns:
        coalition: The coalition that won the election
    """
    def compute_happiness(self, coalition: Coalition) -> float:
        if not self.voted_strategic():
            return None

        happiness = self.party.polled_votes - self.expected_party_seats
        return 2 * happiness if self.voted_for in coalition.parties else happiness


    """
    Creates the profile of the voter based on the party he is initially
    voting for.

    Args:
        party: The party the voter is initially voting for

    returns:
        profile: The profile of the voter
    """
    def create_position(self, party: Party) -> list:
        profile = party.profile.copy()
        for idx, opinion in enumerate(profile):
            strategic_vote_threshold = np.random.uniform(low=0, high=1)
            if strategic_vote_threshold < self.swing:  # Slight opinion change
                if opinion == 0:
                    profile[idx] += np.random.choice([-1, 1])
                elif strategic_vote_threshold <= self.swing / 2:  # Extreme opinion change
                    profile[idx] *= -1
                else:
                    profile[idx] = 0
        return profile


    """
    Compute the score of the voter for each coalition

    Args:
        parties: The list of candidate parties
        coalitions: The list of possible coalitions according to poll

    returns:
        scores: The list of scores for each coalition
    """
    def compute_coalition_scores(self, parties: list, coalitions: list) -> list:
        score_matrix = []
        for party in parties:
            coalitions_with_party = [
                coalition for coalition in coalitions if party in coalition.parties]
            cosine_similarities = [cosine_similarity(self.profile, coalition.profile) \
              for coalition in coalitions_with_party]
            score_matrix.append([cos_similarity * coalition.feasibility if cos_similarity > 0 \
              else 0 for cos_similarity, coalition in zip(cosine_similarities, coalitions_with_party)])

        scores = [len([score for score in score_array if score >
                      0.1])/10 for score_array in score_matrix]
        return scores

