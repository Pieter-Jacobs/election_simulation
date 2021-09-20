from imports import *
import numpy as np


class Voter:
    def __init__(self, party) -> None:
        self.party = party
        self.position = self.generate_position(party) 
        self.swing = np.random.uniform(low=0, high=0.5)

    def vote(self):
        pass

    def compute_ranking(self): 
        pass
    
    def generate_position(self, party):
        zeros = np.zeros(len(party))
        random_vector = [(zeros[i] + np.random.uniform(low=0,high=self.swing)) for i in range(len(zeros))] 
        return self.party + random_vector
        