from imports import *
import numpy as np


class Voter:
    def __init__(self, party, parties) -> None:
        self.party = party
        self.swing = np.random.uniform(low=0, high=0.5)
        self.position = self.generate_position(parties) 
        self.compute_ranking(parties)

    def vote(self):
        pass
    
    def generate_position(self, parties):
        zeros = np.zeros(len(parties))
        random_vector = [(zeros[i] + np.random.uniform(low=0,high=self.swing)) for i in range(len(zeros))] 
        return parties[self.party] + random_vector
    
    def compute_ranking(self, parties): 
        print(self.party)
        cos_sim_matrix = [spatial.distance.cosine(self.position, parties[i]) for i in range(len(parties))]
        ranking = np.argsort(cos_sim_matrix)
        print(ranking)
        return ranking