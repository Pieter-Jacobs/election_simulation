from typing import Protocol
from imports import *
from helpers import cosine_similarity
import numpy as np
from classes.Party import Party


class Voter(object):
    def __init__(self, initial_party, parties, max_swing) -> None:
        self.swing = np.random.uniform(low=0, high=max_swing)
        self.profile = self.create_position(initial_party)
        self.similarities = self.compute_similarities(parties)
        self.party = parties[np.argmax(self.similarities)]
        super().__init__()

    def vote(self, parties, coalitions, residual_seats) -> Party:
        scores = self.similarities + residual_seats + self.compute_coalition_scores(parties, coalitions)
        party = parties[np.argmax(scores)]
        print(party)
        return party

    def compute_similarities(self, parties):
        similarities = np.array([cosine_similarity(
            self.profile, parties[i].profile) for i in range(len(parties))])
        return similarities

    def create_position(self, party):
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

    def compute_coalition_scores(self, parties, coalitions):
        score_matrix = []
        for party in parties:
            coalitions_with_party = [coalition for coalition in coalitions if party in coalition.parties]
            score_matrix.append([cosine_similarity(self.profile, coalition.profile)*coalition.feasibility for coalition in coalitions_with_party])
        scores = [len([score for score in score_array if score>0.1])/10 for score_array in score_matrix]
        return scores