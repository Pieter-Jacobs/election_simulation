from imports import *
from classes.Voter import NR_OF_PARTIES, Voter
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
        Counts the votes for each party and determines the amount of strategic votes, also calculates the number of seats for each party
    init_parties():
        Initialises the parties based hard coded vectors in a text file
    init_voters():
        Initialises voters based on the polls
    calculate_chance_to_influence():
        calculates chances that a vote will make a difference and influence the elections
    """
    NR_OF_PARTIES = 30

    def __init__(self, cfg) -> None:
        """
        Parameters:
        -----------
        cfg: DictConfig 
            Dictionary containing the configuration of the hyperparameters
        """
        self.cfg = cfg
        self.seats_available = cfg.seats
        self.poll_uncertainty = cfg.uncertainty
        self.polls = np.array(cfg.polls.distribution) * cfg.polls.voters
        self.parties = self.init_parties()
        self.voters = self.init_voters(cfg.swing)
        self.calculate_chance_to_influence()
        self.strategic_vote_count = 0

    def count_votes(self):
        """
            Counts and prints the votes for each party and the percentage of strategic votes,
            then counts and prints the number of seats each party obtained.
        """
        print("Counting votes...")
        nr_voters = len(self.voters)
        vote_count = {}
        self.strategic_vote_count = 0
        for voter in self.voters:
            # vote, strategic = voter.vote(self.chances)
            vote, strategic = voter.vote(self.polls, self.seat_influence)
            self.strategic_vote_count += strategic
            if vote not in vote_count.keys():
                vote_count[vote] = 0 
            else:
                vote_count[vote] += 1
        self.vote_percentages = {k: str(v / nr_voters * 100)[:4] + "%" for k, v in vote_count.items()}
        print("Percentage of votes gathered by each party:")
        print(self.vote_percentages)

        if self.seats_available is not None:
            votes_for_seat = nr_voters / self.seats_available
            seats = {k: v // votes_for_seat for k, v in vote_count.items()} 
            seats_occupied = sum([val for val in seats.values()])

            while seats_occupied < self.seats_available:
              max_ratio = -1
              party = -1
              for k, v in vote_count.items():
                  if v / (seats[k] + 1) > max_ratio:
                      party = k
                      max_ratio = v / (seats[k] + 1)
              seats[party] += 1
              seats_occupied += 1

            print("Seats for each party")
            print(seats)
            self.seats = seats

        print("Percentage of strategic votes:")
        print(str(self.strategic_vote_count / nr_voters * 100) + '%')


    def init_parties(self):
        """Initialises the parties based hard coded vectors in a text file"""
        parties = np.genfromtxt(hydra.utils.get_original_cwd(
        ) + os.path.sep + 'party_vector.csv', delimiter=',')
        return parties


    def init_voters(self, max_swing):
        """Initialises voters based on the polls"""
        self.swing = max_swing
        Voter.set_switches()
        voters = [Voter(i, self.parties, max_swing) for i in range(len(self.polls)) for j in range(int(self.polls[i]))]
        return voters
        

    def calculate_chance_to_influence(self):
        """ 
            Calculates the expected chance of a vote to make a difference, based upon the parties poll rankings, 
            and calculates the expected influence of a vote to take an extra seat.
        """
    # if self.seats_available is None:
        poll_uncertainty = 0.5   # Parameter indicating uncertainty in the poll / Maybe put in config
    # else:
        votes_per_seat = len(self.voters) / self.seats_available
        self.seat_influence = np.zeros(Election.NR_OF_PARTIES)

        for idx, poll_result in enumerate(np.nditer(self.polls)):
            self.seat_influence[idx] = (poll_result % votes_per_seat) / votes_per_seat

        most_votes = np.max(self.polls)
        self.chances = np.zeros(Election.NR_OF_PARTIES)

        for idx, poll_result in enumerate(np.nditer(self.polls)):
            sigma = poll_result * poll_uncertainty
            if sigma == 0:
                sigma = 0.001

           saver polls
        return


