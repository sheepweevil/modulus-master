""" A unit test for the sumoku.game module """
import unittest
from sumoku import game


class TestGame(unittest.TestCase):
    """ Test implementation of game rules """

    def test_validate_play(self):
        """ Tests play validation """
        # This should fail because the sum doesn't match
        self.assertRaises(game.InvalidPlayException,
                          game.validate_play, [(1, 0)], 3)

        # This should fail because it has two of the same color
        self.assertRaises(game.InvalidPlayException,
                          game.validate_play, [(1, 0), (2, 0)], 3)

        # This should succeed
        self.assertTrue(game.validate_play([(1, 0), (2, 1)], 3))

    def test_draw_tile(self):
        """ Tests drawing tiles """
        tiles = [(1, 0), (2, 0)]
        tile1 = game.draw_tile(tiles)
        self.assertEqual(len(tiles), 1)
        tile2 = game.draw_tile(tiles)
        self.assertEqual(len(tiles), 0)
        self.assertRaises(IndexError, game.draw_tile, tiles)

        # Check numbers
        self.assertTrue(tile1[0] == 1 or tile1[0] == 2)
        if tile1[0] == 1:
            self.assertEquals(tile2[0], 2)
        else:
            self.assertEquals(tile2[0], 1)

        # Check colors
        self.assertEquals(tile1[1], 0)
        self.assertEquals(tile2[1], 0)
