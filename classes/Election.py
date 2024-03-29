from imports import *
from classes.Party import Party
from classes.Voter import Voter
from classes.Coalition import Coalition
import numpy as np


class Election(object):
    """ 
    Defines a class that is used to run a simulation of a democratic election

    Attributes:
    -----------
    polls: list of int
        The percentage of votes polled for each party 
    parties: list of Party
        The parties involved in the election
    voters: list of Voter
        The Voters involved in the election

    Methods
    -------
    start():
        Starts the election
    compute_residual_seats(self) -> list:
        Computes the residual seats
    determine_seats() -> list:
        Determines the seats
    count_votes():
        Counts the votes for each party and determines the amount of strategic votes, also calculates the number of seats for each party
    create_parties():
        Initialises the parties based hard coded vectors in a text file
    create_voters():
        Initialises voters based on the polls
    create_coalitions():
        Creates the coalitions based upon the parties and polls
    calculate_chance_to_influence():
        calculates chances that a vote will make a difference and influence the elections
    average_happiness(self) -> float:
        Calculates the average happiness of the voters
    most_feasible_coalition(self) -> Coalition:
        Returns the most feasible coalition
    """

    def __init__(self, n_seats: int, n_voters: int, polls: DictConfig, upper_swing: float) -> None:
        super().__init__()
        self.n_seats = n_seats
        self.n_voters = n_voters
        self.polls = np.array(polls)
        self.parties = self.create_parties()
        self.voters = self.create_voters(upper_swing)
        self.coalition = None

    def start(self):
        """
        Start the election

        returns:
            The distribution of seats after the election
        """
        self.coalitions = self.create_coalitions()
        strategic_vote_count = 0
        n_parties = len(self.parties)
        votes = {i: 0 for i in range(n_parties)}
        vote_switches = [[0 for _ in range(n_parties)]
                         for _ in range(n_parties)]
        for idx, voter in enumerate(self.voters):
            if idx % (self.n_voters / 10) == 0:
                print(idx)

            vote = voter.vote(parties=self.parties, coalitions=self.coalitions,
                              residual_seats=self.compute_residual_seats())
            votes[vote.mapping] += 1
            vote_switches[voter.party.mapping][vote.mapping] += 1
            strategic_vote_count += voter.voted_strategic()

        seats = self.determine_seats(votes)

        for k, v in votes.items():
            self.polls[k] = v / self.n_voters
        # update polled votes for parties
        for party in self.parties:
            party.polled_votes = self.polls[party.mapping]

        return list(seats.values()), vote_switches, (strategic_vote_count / sum(votes.values())) * 100

    def compute_residual_seats(self) -> list:
        """
        Compute the seats mod 1 to obtain the residual seats
        """
        seats = self.polls * self.n_seats
        return np.array(seats) % 1

    def determine_seats(self, results) -> list:
        """
        Determine the seat distribution after the voting has closed
        
        Args:
            results: list of the votes

        Returns:
            The seat distribution
        """
        seats = {k: 0 for k in range(30)}
        votes = np.array(list(results.values()))
        electoral_quotient = sum(votes) / self.n_seats
        for party in range(len(votes)):
            party_votes = votes[party].copy()
            while party_votes >= electoral_quotient:
                seats[party] += 1
                party_votes -= electoral_quotient

        averages = [votes[party] / (seats[party] + 1)
                    for party in range(len(votes))]
        while sum(list(seats.values())) < self.n_seats:
            largest = np.argmax(averages)
            seats[largest] += 1
            averages[largest] = votes[largest] / (seats[largest] + 1)
        return seats

    def create_parties(self) -> list:
        """
        Initialise the parties

        returns:
            The parties
        """
        profiles = np.genfromtxt(hydra.utils.get_original_cwd(
        ) + os.path.sep + 'party_profiles.csv', delimiter=',')
        parties = [Party(profile=profile, polled_votes=polled_votes, mapping=i)
                   for i, (profile, polled_votes) in enumerate(zip(profiles, self.polls))]
        return parties

    def create_voters(self, upper_swing: float) -> list:
        """
        Initialize the voters

        returns:
            The voters
        """
        voters = [Voter(initial_party=self.parties[i], parties=self.parties, upper_swing=upper_swing) for i in range(len(self.polls))
                  for j in range(int(self.polls[i]*self.n_voters))]
        return voters

    def create_coalitions(self) -> list:
        """
        Initialise the coalitions
        
        returns:
            The coalitions
        """
        self.coalitions = self.find_coalitions()
        self.coalitions.sort(
            key=lambda coalition: coalition.feasibility, reverse=True)

        return self.coalitions

    def find_coalitions(self, current_parties=[], current_idx=0) -> list:
        """
        Find the possible coalitions based on the following criteria:
            - The coalition must have over half of the seats
            - The coalition cannot miss a single party and still have over half of the seats
            - The coalition has no more than 5 parties
        """
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

    def most_feasible_coalition(self) -> Coalition:
        """
        Find most feasible coalition
        """
        return max(self.coalitions, key=lambda coalition: coalition.feasibility)

    def average_happiness(self) -> float:
        """
        Find average happiness of all voters
        """
        coalition = self.__most_feasible_coalition()
        return average([voter.compute_happiness(coalition) for voter in self.voters if voter.voted_strategic()])
