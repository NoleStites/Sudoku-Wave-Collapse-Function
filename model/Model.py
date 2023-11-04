from tile.Tile import Tile # For type verification
from typing import List
from random import choice

class Model():
    
    def getValidTiles(self, tile_grid: List[List[Tile]]):
        """
        Iterates through each Tile in the grid and determines if it
        has collapsed or not, then returns a list of uncollapsed Tiles
        with the lowest entropy; if all are collapsed, returns None.
        """
        grid_size = len(tile_grid)
        
        valid_tiles = []
        lowest_entropy = grid_size

        for column in range(grid_size):
            for row in range(grid_size):
                tile = tile_grid[column][row]
                if not(tile.collapsed):
                    valid_tiles.append(tile)
                    # Update lowest entropy if new lowest is found
                    if (len(tile.entropy) < lowest_entropy) and (len(tile.entropy) != 0):
                        lowest_entropy = len(tile.entropy)


        # Before returning the list, verify that it isn't empty
        if len(valid_tiles) == 0:
            return None

        # Only return the Tiles with entropy = lowest_entropy
        new_valid_tiles = []
        for tile in valid_tiles:
            if len(tile.entropy) == lowest_entropy:
                new_valid_tiles.append(tile)

        if len(new_valid_tiles) == 0:
            return None

        return new_valid_tiles


    def chooseRandomTile(self, valid_tiles: List[Tile]):
        """
        Given a list of uncollapsed tiles, this method will choose a
        random tile and, for that tile, a random value and return them.
        """
        random_tile = choice(valid_tiles)

        return random_tile

    
    def chooseRandomValue(self, tile: Tile, exclude: List[int]):
        """
        Given a Tile, will return a random value from its entropy list
        that is not included in the exclude list.

        Returns None if there are no values to choose from after the exclusions.
        """
        # Before choosing, remove values that must be excluded
        smaller_entropy_list = tile.entropy.copy()
        for val_to_remove in exclude:
            while smaller_entropy_list.count(val_to_remove) > 0:
                smaller_entropy_list.remove(val_to_remove)

        # Verify that list isn't empty
        if len(smaller_entropy_list) == 0:
            return None

        # Choose and return a random value from the new entropy list
        random_value = choice(smaller_entropy_list)
        return random_value


    def produceGamifyTiles(self, num_to_produce: int, tile_grid: List[List[Tile]]):
        """
        Chooses a number of random coords in the grid boundaries
        based on the parameter num_to_produce.
        Returns a list of (x, y) tuples.
        """
        # Produce a list of all tiles
        all_tiles = []

        grid_length = len(tile_grid)
        for column in range(grid_length):
            for row in range(grid_length):
                all_tiles.append(tile_grid[column][row])

        # Pick num_to_produce Tiles out of the list
        chosen_tiles = []

        for i in range(num_to_produce):
            chosen_tile = choice(all_tiles)     # Chose a random tile from the list
            all_tiles.remove(chosen_tile)       # Remove it from the list so it isn't chosen again
            chosen_tiles.append(chosen_tile)    # Add chosen tile to list of chosen tiles

        # Create a list of coordinates to be returned
        coords = []

        for tile in chosen_tiles:
            coords.append(tile.coord)

        return coords




