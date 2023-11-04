from model.Model import Model
from typing import List
from tile.Tile import Tile # For type verification

class Controller():

    def __init__(self, model: Model):
        self.model = model

    
    def randomTile(self, tile_grid: List[List[Tile]]):
        """
        Given the two-dimensional list of Tiles, determines
        which tiles are uncollapsed and have the lowest entropy.

        Returns a random Tile.
        If there are no uncollasped Tiles, return None.
        """
        # Get a list of uncollapsed Tiles with the lowest entropy to choose from
        valid_tiles = self.model.getValidTiles(tile_grid)
        if valid_tiles == None:
            return None

        # Choose random Tile to be returned
        tile_v = self.model.chooseRandomTile(valid_tiles)

        return tile_v


    def randomValue(self, tile: Tile, exclude=[]):
        """
        Given a Tile and, optionally, a list of values to exclude,
        will return an integer to be displayed inside the Tile.
        """
        value = self.model.chooseRandomValue(tile, exclude)
        return value


    def getGamifyTiles(self, num_to_remove: int, tile_grid: List[List[Tile]]):
        """
        Has the model produce a list of unique Tile coordinates.
        Returns a list of (x, y) tuples.
        """
        # Get list of Tile coords from the model
        tile_coords = self.model.produceGamifyTiles(num_to_remove, tile_grid)

        return tile_coords
