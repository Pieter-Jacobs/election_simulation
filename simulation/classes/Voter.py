from imports import *
import numpy as np

@njit
def cosine_similarity(v1,v2):
    """Compute the cosine similarity between vectors v1 and v2"""
    sumxx, sumxy, sumyy = 0, 0, 0
    for i in range(len(v1)):
        x = v1[i]; y = v2[i]
        sumxx += x*x
        sumyy += y*y
        sumxy += x*y
    return sumxy/((sumxx**0.5)*(sumyy**0.5))


class Voter:
    def __init__(self, party, parties) -> None:
        self.party = party
        self.swing = np.random.uniform(low=0, high=1)
        self.position = self.generate_position(parties)
        self.similarities = self.compute_similarities(parties)

    def vote(self, polls):
        scores = self.similarities * polls
        party = np.argmax(scores)
        return party
    
    def generate_position(self, parties):
        zeros = np.zeros(len(parties[self.party]))
        random_vector = [(zeros[i] + np.random.uniform(low=-self.swing,high=self.swing)) for i in range(len(zeros))] 
        return parties[self.party] + random_vector
    
    def compute_similarities(self, parties):
        cos_sim_matrix = np.array([cosine_similarity(self.position, parties[i]) for i in range(len(parties))])
        return cos_sim_matrix

    def compute_formation_score(self, polls):
        pass