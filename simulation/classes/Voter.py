from imports import *
import numpy as np


class Voter:
    def __init__(self, uncertainty, party) -> None:
        self.party = party
        self.position = self.generate_position(party) 
        self.swing = np.random.uniform(low=0, high=0.5)
        pass

    def vote(self):
        pass

    def compute_ranking(self): 
        pass
    
    def generate_position(self, party):
        print(self.party + np.random.rand(len(party)))
        return self.party + np.random.rand(len(party))
        