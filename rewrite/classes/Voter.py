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
        super().__init__()


    def vote(self, parties: list, coalitions: list, residual_seats: list) -> Party:
        scores = self.similarities + residual_seats + \
            self.compute_coalition_scores(parties, coalitions)
        party = parties[np.argmax(scores)]
        return party


    def compute_similarities(self, parties: list) -> list:
        similarities = np.array([cosine_similarity(
            self.profile, parties[i].profile) for i in range(len(parties))])
        return similarities


    # Find voter happiness with coalition
    def compute_happiness(self, coalition: Coalition) -> float:
        return cosine_similarity(self.profile, coalition.profile)


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
        scores = []
        for party in parties:
            coalitions_with_party = [
                coalition for coalition in coalitions if party in coalition.parties]
            if coalitions_with_party == []:
                scores.append(0)
                continue

            scores.append(max([cosine_similarity(self.profile, coalition.profile) for coalition in coalitions_with_party]))
              # weights=[coalition.feasibility for coalition in coalitions_with_party]))

        Voter.coal_scores[np.argmax(scores)] += 1
        return scores

    # def compute_coalition_scores(self, parties: list, coalitions: list) -> list:
    #     score_matrix = []
    #     print(len(parties))
    #     for party in parties:
    #         coalitions_with_party = [
    #             coalition for coalition in coalitions if party in coalition.parties]
    #         score_matrix.append([cosine_similarity(self.profile, coalition.profile)
    #                             * coalition.feasibility for coalition in coalitions_with_party])
    #     scores = [sum(score_array) for score_array in score_matrix]
    #     print(np.argmax(scores))
    #     return scores

