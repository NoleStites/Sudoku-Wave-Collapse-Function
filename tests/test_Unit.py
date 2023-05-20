
import unittest
from tests.fakeTile import FakeTile
from model.Model import Model

"""
I had some difficulties finding methods within my program to test because
most of them (in the model at least) involved randomization and you can't
really test a result if you have no idea what it is.

All of my other class methods in, say, the controller and view all involve
my GUI and the special variables associated with it, so it wasn't very easy
to find testable methods.

I trust that the GUI works nicely, though! And with the logger in place, it
acts as a sort of catcher-of-bugs for certain things.
"""

class TestMVC(unittest.TestCase):

    def test_model_getValidTiles(self):
        """
        Tests the getValidTiles() method of the model.

        getValidTiles() should return a list of Tiles that
        are not collapsed and have the least entropy compared
        to all other Tiles.
        """
        # Make a sample of fake entropy lists
        a1 = [2]
        a2 = [22]
        b = [3, 4]
        c = [5, 6, 7]
        d = [8, 9, 10, 11]

        # Create a few fake Tiles to pass to getValidTiles()
        tile_list = [
            [FakeTile(True, a1), FakeTile(True, b), FakeTile(True, c)],
            [FakeTile(True, d), FakeTile(False, a1), FakeTile(False, d)],
            [FakeTile(False, b), FakeTile(False, c), FakeTile(False, a2)]
        ]

        # Call the method and check results
        model = Model()
        results = model.getValidTiles(tile_list)

        for tile in results:
            self.assertEqual(tile.collapsed, False)
            self.assertEqual(len(tile.entropy), 1)

    



