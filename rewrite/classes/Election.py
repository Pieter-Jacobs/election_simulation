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
        self.polls = np.array(polls)
        self.parties = self.create_parties()
        self.voters = self.create_voters(max_swing)
        self.coalitions = self.create_coalitions()

    def start(self):
        strategic_vote_count = 0
        n_parties = len(self.parties)
        votes = {i: 0 for i in range(n_parties)}
        vote_switches = [[0 for _ in range(n_parties)]
                         for _ in range(n_parties)]

        for voter in self.voters:
            vote = voter.vote(parties=self.parties, coalitions=self.coalitions,
                              residual_seats=self.compute_residual_seats())
            votes[vote.mapping] += 1
            vote_switches[voter.party.mapping][vote.mapping] += 1
            strategic_vote_count += voter.party == vote
        #strategic_vote_count = sum([vote for i, party_switches in enumerate(vote_switches) for j, vote in enumerate(party_switches) if i != j])
        results = {k: (v / len(self.voters)) * 100 for k, v in votes.items()}
        results_seats = {k: (v * self.n_seats) for k, v in results.items()}
        print(results)
        print(strategic_vote_count)
        pass

    def compute_residual_seats(self) -> list:
        seats = self.polls * self.n_seats
        return np.array(seats) % 1

    def create_parties(self) -> list:
        profiles = np.genfromtxt(hydra.utils.get_original_cwd(
        ) + os.path.sep + 'party_profiles.csv', delimiter=',')
        parties = [Party(profile=profile, polled_votes=polled_votes, mapping=i)
                   for i, (profile, polled_votes) in enumerate(zip(profiles, self.polls))]
        return parties

    def create_voters(self, max_swing) -> list:
        voters = [Voter(initial_party=self.parties[i], parties=self.parties, max_swing=max_swing) for i in range(len(self.polls))
                  for j in range(int(self.polls[i]*self.n_voters))]
        print(len(voters))
        return voters

    def create_coalitions(self) -> list:
        coalitions = self.find_coalitions()
        coalitions.sort(
            key=lambda coalition: coalition.feasibility, reverse=True)
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
