from imports import *
from classes.Voter import Voter

class Election: 
    def __init__(self, n_voters) -> None:
        self.voters = generate_voters()
        pass
    
    def generate_voters(n_voters):
        voters = []
        for i in range(n_voters):
            voter = Voter()
            voters.append(voter)
        pass