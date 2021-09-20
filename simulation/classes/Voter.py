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
        self.swing = np.random.uniform(low=0, high=0.5)
        self.position = self.generate_position(parties)
        self.ranking, self.cos_sim_ranking = self.compute_ranking(parties)

    def vote(self, polls):
        
        return
    
    def generate_position(self, parties):
        zeros = np.zeros(len(parties))
        random_vector = [(zeros[i] + np.random.uniform(low=0,high=self.swing)) for i in range(len(zeros))] 
        return parties[self.party] + random_vector
    
    def compute_ranking(self, parties):
        cos_sim_matrix = np.array([cosine_similarity(parties[6], parties[i]) for i in range(len(parties))])
        cos_sim_ranking = sorted(cos_sim_matrix, reverse=True)
        print(cos_sim_matrix)
        ranking = np.argsort(-cos_sim_matrix)
        return ranking, cos_sim_ranking

    def compute_formation_score(self, polls):
        pass