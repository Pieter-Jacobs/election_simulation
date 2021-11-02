from typing import Protocol
from imports import *
from helpers import cosine_similarity
import numpy as np

class Voter(object):
    parties = None
    max_swing = None

    def __init__(self, initial_party) -> None:
        self.swing = np.random.uniform(low=0, high=Voter.max_swing)
        self.profile = self.create_position(initial_party)
        self.similarities = self.compute_similarities()
        self.party = Voter.parties[np.argmax(self.similarities)]
        super().__init__()
    
    def vote():
        pass
    
    def compute_similarities(self):
        similarities = np.array([cosine_similarity(self.profile, Voter.parties[i].profile) for i in range(len(Voter.parties))])
        return similarities

    def create_position(self, party):
        profile = party.profile.copy()
        for idx, opinion in enumerate(profile):
            strategic_vote_threshold = np.random.uniform(low = 0, high = 1)
            if strategic_vote_threshold < self.swing: # Slight opinion change 
                if opinion == 0:
                    profile[idx] += np.random.choice([-1,1])    
                elif strategic_vote_threshold <= self.swing / 2: # Extreme opinion change 
                    profile[idx] *= -1   
                else:
                    profile[idx] = 0
        return profile