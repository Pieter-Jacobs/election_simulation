from typing import Mapping
from imports import *

class Party(object):
    def __init__(self, profile, polled_votes, mapping) -> None:
        self.profile = profile
        self.polled_votes = polled_votes
        self.mapping = mapping
        super().__init__()

    def __str__(self) -> str:
        return str(self.mapping)
