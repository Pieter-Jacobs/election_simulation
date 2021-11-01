import numpy
from numpy.lib.function_base import average
from helpers import *
import sys

sys.setrecursionlimit(5000)

class Coalition:
    party_vectors = None

    def __init__(self, parties, polls):
        self.parties = parties
        self.polls = polls
        self.feasibility = self.coalition_feasibility(parties)
        self.profile = self.coalition_profile()


    def coalition_profile(self) -> numpy.ndarray:
        profile = []
        if len(self.parties) == 1:
            return self.parties[0]

        for idx in range(Coalition.party_vectors[0].shape[0]):
            stance = [] 
            for party in self.parties:
                stance += [Coalition.party_vectors[party][idx]]
            profile += [numpy.average(stance, weights=self.polls)]
        return numpy.asarray(profile)


    def coalition_feasibility(self, parties: list) -> float:
        return average([cosine_similarity(Coalition.party_vectors[j], Coalition.party_vectors[i]) for idx, i in enumerate(parties[:-1])\
                                                                                                  for j      in parties[idx+1:]])


    def __str__(self) -> str:
        return str(self.parties) + "\t" + str(self.feasibility)


    @staticmethod
    def init_coalitions(parties, polls, cur_parties = [], cur_idx = 0):
        if sum([(polls[cur_party]) for cur_party in cur_parties]) >= 0.5:
            return [cur_parties]
        if len(cur_parties) >= 5 or len(parties) == 0: 
            return []

        coalitions = []
        coalitions += Coalition.init_coalitions(parties[1:], polls, cur_parties, cur_idx + 1)
        coalitions += Coalition.init_coalitions(parties[1:], polls, cur_parties + [cur_idx], cur_idx + 1)


        if cur_idx != 0:
          return coalitions

        new_coalitions = []
        for coalition in coalitions:
            coal_polls = [polls[party] for party in coalition]
            if sum(coal_polls) - min(coal_polls) <= 0.5:
                new_coalitions += [Coalition(coalition, coal_polls)]

        new_coalitions.sort(key=lambda x:x.feasibility, reverse=True)
        for coalition in new_coalitions:
            print(coalition)

        return new_coalitions

