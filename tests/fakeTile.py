
from typing import List


class FakeTile():
    """
    For testing purposes, this class will represent a fake Tile object
    that only has the collapsed and entropy attributes.
    """
    def __init__(self, collapsed: bool, entropy: List[int]):
        self.collapsed = collapsed
        self.entropy = entropy
