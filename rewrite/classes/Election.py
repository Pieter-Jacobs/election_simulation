from imports import *
from classes.Party import Party
from classes.Voter import Voter
from classes.Coalition import Coalition
import numpy as np


class Election(object):
    def __init__(self, n_seats, n_voters, polls, max_swing) -> None:
        super().__init__()
        self.n_seats = n_seats
        self.n_voters = n_voters
        self.polls = polls
        self.parties = self.create_parties()
        self.voters = self.create_voters(max_swing)
        self.coalitions = self.create_coalitions()

    def create_parties(self) -> list:
        profiles = np.genfromtxt(hydra.utils.get_original_cwd(
        ) + os.path.sep + 'party_profiles.csv', delimiter=',')
        parties = [Party(profile=profile, polled_votes=polled_votes, mapping=i)
                   for i, (profile, polled_votes) in enumerate(zip(profiles, list(self.polls)))]
        return parties

    def create_voters(self, max_swing) -> list:
        Voter.max_swing = max_swing
        Voter.parties = self.parties
        voters = [Voter(initial_party=self.parties[i]) for i in range(len(self.polls))
                  for j in range(int(self.polls[i]*self.n_voters))]
        print(voters[0].profile)
        return voters

    def create_coalitions(self) -> list:
        coalitions = self.find_coalitions()
        coalitions.sort(key=lambda coalition: coalition.feasibility, reverse=True)
        print(coalitions[0])
        return coalitions

    def find_coalitions(self, current_parties=[], current_idx=0) -> list:
        polls = [party.polled_votes for party in current_parties]
        polled_votes = sum(polls)
        # Base case: the parties can form a coalition and all parties are necassary
        if polled_votes >= 0.5 and polled_votes - min(polls) <= 0.5:
            return [Coalition(current_parties)]
        # Base Case: no coalition can be formed
        if len(current_parties) >= 5 or current_idx == len(self.parties):
            return []

        coalitions = self.find_coalitions(current_parties, current_idx + 1) + \
            self.find_coalitions(
                current_parties + [self.parties[current_idx]], current_idx + 1)

        return coalitions
