from model.Model import Model
from typing import List
from tile.Tile import Tile # For type verification

class Controller():

    def __init__(self, model: Model):
        self.model = model

    
    def randomTileAndValue(self, tile_grid: List[List[Tile]]):
        """
        Given the two-dimensional list of Tiles, determines
        which tiles are uncollapsed and have the lowest entropy.

        Returns a random Tile and value to assign to it.
        If there are no uncollasped Tiles, return None.
        """
        # Get a list of uncollapsed Tiles to choose from
        valid_tiles = self.model.getValidTiles(tile_grid)
        if valid_tiles == None:
            return None

        # Update valid_tiles by only including ones with the lowest entropy

        # Choose random Tile and value to be returned
        tile_v = self.model.chooseRandomTileAndValue(valid_tiles)

        return tile_v


    def getGamifyTiles(self, num_to_remove: int, tile_grid: List[List[Tile]]):
        """
        Has the model produce a list of unique Tile coordinates.
        Returns a list of (x, y) tuples.
        """
        # Get list of Tile coords from the model
        tile_coords = self.model.produceGamifyTiles(num_to_remove, tile_grid)

        return tile_coords
