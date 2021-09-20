from imports import *
from classes.Voter import Voter
import numpy as np

class Election: 
    def __init__(self) -> None:
        self.parties = self.init_parties()
        #self.voters = self.init_voters()
        pass
    
    def init_parties(self):
        parties = np.genfromtxt(hydra.utils.get_original_cwd() + os.path.sep + 'party_vector.csv', delimiter = ',')
        print(parties)
        
        return parties

    # def init_voters(n_voters):
    #     voters = []
    #     for i in range(n_voters):
    #         voter = Voter()
    #         voters.append(voter)
    #     pass