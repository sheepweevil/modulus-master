""" A unit test for the sumoku.game module """
import unittest
from sumoku import game


class TestGame(unittest.TestCase):
    """ Test implementation of game rules """

    def test_score_tiles(self):
        """ Test play validation """
        # This should fail because the sum doesn't match
        self.assertRaises(game.InvalidPlayException,
                          game.score_tiles, [(1, 0), (4, 0)], 3)

        # This should fail because it has two of the same color
        self.assertRaises(game.InvalidPlayException,
                          game.score_tiles, [(1, 0), (2, 0)], 3)

        # This should succeed
        self.assertEqual(game.score_tiles([(1, 0), (2, 1)], 3), 3)
        self.assertEqual(game.score_tiles([(1, 0)], 3), 0)

    def test_draw_tile(self):
        """ Test drawing tiles """
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

    def test_complete_line(self):
        """ Test completing a line with tiles on the board """

        # Nothing to complete for only one tile
        tile = (1, 0, 0, 0)
        self.assertEquals(game.complete_line(tile, True, []), [tile])
        self.assertEquals(game.complete_line(tile, False, []), [tile])

        # Test completion on row and column
        xtile = (2, 0, 1, 0)
        ytile = (2, 0, 0, 1)
        board = [xtile, ytile]
        self.assertEquals(game.complete_line(tile, True, board),
                          [tile, xtile])
        self.assertEquals(game.complete_line(tile, False, board),
                          [tile, ytile])
        aftertile = (1, 0, 1, 1)
        self.assertEquals(game.complete_line(aftertile, True, board),
                          [aftertile, ytile])
        self.assertEquals(game.complete_line(aftertile, False, board),
                          [aftertile, xtile])

    def test_get_key_number(self):
        """ Test getting a random key number """
        keynum = game.get_key_number()
        self.assertTrue(keynum < 6)
        self.assertTrue(keynum > 2)

    def test_score_play(self):
        """ Test scoring a play """
        # Test various invalid plays
        self.assertRaises(game.InvalidPlayException, game.score_play,
                          [(1, 0, 0, 0)], [], 3)
        self.assertRaises(game.InvalidPlayException, game.score_play,
                          [(1, 0, 0, 0), (1, 0, 1, 1)], [], 3)
        self.assertRaises(game.InvalidPlayException, game.score_play,
                          [(1, 0, 0, 0), (1, 0, 0, 2)], [], 3)

        # Now some valid plays
        self.assertEqual(game.score_play([(3, 0, 0, 0)], [], 3), 3)
        origin = (1, 0, 0, 0)
        xtile = (2, 1, 1, 0)
        ytile = (2, 1, 0, 1)
        self.assertEqual(game.score_play([origin, xtile], [], 3), 3)
        self.assertEqual(game.score_play([origin, ytile], [], 3), 3)
        self.assertEqual(game.score_play([origin], [xtile], 3), 3)
        self.assertEqual(game.score_play([origin], [ytile], 3), 3)
        self.assertEqual(game.score_play([origin, xtile], [ytile], 3), 6)
        self.assertEqual(game.score_play([origin, ytile], [xtile], 3), 6)
        self.assertEqual(game.score_play([origin], [xtile, ytile], 3), 6)
