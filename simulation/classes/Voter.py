from imports import *
import numpy as np
from helpers import *

NR_OF_PARTIES = 30



class Voter:
    """ 
    Defines a class that represents a voter in a democratic election

    Attributes:
    -----------
    party: list of int
        The political party the voter feels best represents his or her ideals
    swing: float
        The amount of uncertainty the voter has associated to the party that best represents his or her ideals
    position: list of int
        The position of the voter in vector space that represents his or her political stance
    similarities: list of float
        The cosine similarity of the voters position in vector space to that of all political parties

    Methods
    -------
    vote():
        Determines the voting scores associated with the parties and returns the party with the highest score
    generate_position():
        Generates and returns the position of the agent in vector state through slightly changing the vector of the voters preferred party
    compute_voter_similarities():
        Computes and returns the cosine similarities of the agents position with all political parties in the election
    """
    ## Static data
    switches = [[0 for _ in range(NR_OF_PARTIES)] for _ in range(NR_OF_PARTIES)]

    def __init__(self, party, parties, max_swing) -> None:
        self.party = party
        self.swing = np.random.uniform(low=0, high=max_swing)
        self.importance_of_seats = np.random.uniform(0, 1)
        self.position = self.generate_position(parties)
        self.similarities = self.compute_voter_similarities(parties)
        self.party = np.argmax(self.similarities)
        self.compute_coalition_score(parties)

    def vote(self, polls, seats, party_similarities):
        scores = self.similarities * ((1 - self.importance_of_seats) * polls + (self.importance_of_seats * seats))
        party = np.argmax(scores)
        Voter.switches[self.party][party] += 1
        return party, party != self.party
    
    # def generate_position(self, parties):
    #     zeros = np.zeros(len(parties[self.party]))
    #     random_vector = [(zeros[i] + np.random.uniform(low=-self.swing,high=self.swing)) for i in range(len(zeros))] 
    #     return parties[self.party] + random_vector


    def generate_position(self, parties):
        voter_vector = parties[self.party].copy()
        for party, opinion in enumerate(parties[self.party]):
            strategic_vote_threshold = np.random.uniform(low = 0, high = 1)
            if strategic_vote_threshold < self.swing: # Slight opinion change 
                if opinion == 0:
                    voter_vector[party] += np.random.choice([-1,1])    
                elif strategic_vote_threshold <= self.swing / 2: # Extreme opinion change 
                    voter_vector[party] *= -1   
                else:
                    voter_vector[party] = 0
        return voter_vector


    def compute_voter_similarities(self, parties):
        cos_sim_matrix = np.array([cosine_similarity(self.position, parties[i]) for i in range(len(parties))])
        return cos_sim_matrix
    
    def compute_party_similarities(self, parties):
        cos_sim_matrix = np.array([[cosine_similarity(parties[i], parties[j]) for i in range(len(parties))] for j in range(len(parties))])
        return cos_sim_matrix

    def compute_coalition_score(self, parties):
        voter_similarities = self.compute_voter_similarities(parties)
        party_similarities = self.compute_party_similarities(parties)
        
        pass

    @staticmethod
    def switch_matrix() -> str:
        to_return = ""
        for row in Voter.switches:
            for entry in row:
                to_return += '{0: >5}'.format(entry) + "|"
            to_return += '\n'

        return to_return

    @staticmethod
    def set_switches():
        Voter.switches = [[0 for _ in range(NR_OF_PARTIES)] for _ in range(NR_OF_PARTIES)]