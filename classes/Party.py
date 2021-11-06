from typing import Mapping
from imports import *


class Party(object):
    """
    A class representing a candidate party in an election.
    No behaviour implemented, only contains the following data:

      self.profile: A list of the candidate's profile.
      self.polled_votes: A list of the candidate's votes.
      self.mapping: The candidate's index in the party list.
    """

    def __init__(self, profile: list, polled_votes: list, mapping: int) -> None:
        self.profile = profile
        self.polled_votes = polled_votes
        self.mapping = mapping
        super().__init__()

    def __str__(self) -> str:
        return str(self.mapping)
