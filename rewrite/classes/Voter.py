from imports import *
from helpers import cosine_similarity
import numpy as np
from classes.Party import Party
from classes.Coalition import Coalition


class Voter(object):
    coal_scores = {i : 0 for i in range(30)}

    def __init__(self, initial_party: Party, parties: list, upper_swing: float) -> None:
        self.swing = np.random.uniform(low=0, high=upper_swing)
        self.profile = self.create_position(initial_party)
        self.similarities = self.compute_similarities(parties)
        self.party = parties[np.argmax(self.similarities)]
        self.expected_party_seats = 0
        super().__init__()


    def vote(self, parties: list, coalitions: list, residual_seats: list) -> Party:
        scores = self.similarities + residual_seats + \
            self.compute_coalition_scores(parties, coalitions)
        party = parties[np.argmax(scores)]
        self.voted_for = party
        self.expected_party_seats = party.polled_votes
        return party


    def compute_similarities(self, parties: list) -> list:
        similarities = np.array([cosine_similarity(
            self.profile, parties[i].profile) for i in range(len(parties))])
        return similarities
    

    # Check if voter voted strategically
    def voted_strategic(self) -> bool:
        return self.voted_for != self.party


    # Find voter happiness with coalition
    def compute_happiness(self, coalition: Coalition) -> float:
        if not self.voted_strategic():
            return None

        happiness = self.party.polled_votes - self.expected_party_seats
        return 2 * happiness if self.voted_for in coalition.parties else happiness


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

