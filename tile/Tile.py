from tkinter import Frame, Label


class Tile():
    """
    This class stores data on each individual tile in the tile grid.
    """
    def __init__(self, frame: Frame, label: Label, subsquare: (int), tiles: int, x: int, y: int):
        self.frame = frame
        self.label = label  # The tile image displayed
        self.subsquare = subsquare
        self.entropy = [ num+1 for num in range(tiles) ]    # Numbers that are allowed to go in the given Tile
        self.collapsed = False
        self.coord = (x, y)
