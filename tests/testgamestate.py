""" A unit test for sumoku game state """
import unittest
from sumoku import game, gamestate


class TestGameState(unittest.TestCase):
    """ Test game state manipulation """

    def test_init(self):
        """ Test the initial game state """
        state = gamestate.GameState(2, 8, 3)
        self.assertEqual(state.players, 2)
        self.assertEqual(state.hand_size, 8)
        self.assertEqual(state.key_number, 3)
        self.assertEqual(len(state.tiles), 80)
        self.assertEqual(len(state.hands), 2)
        self.assertEqual(len(state.hands[0]), 8)
        self.assertEqual(len(state.hands[1]), 8)
        self.assertEqual(len(state.scores), 2)
        self.assertEqual(state.scores[0], 0)
        self.assertEqual(state.scores[1], 0)
        self.assertEqual(len(state.played_tiles), 0)
        self.assertEqual(len(state.pending_tiles), 0)
        self.assertEqual(state.player, 0)

    def test_cur_hand(self):
        """ Test getting the current hand """
        state = gamestate.GameState(2, 8, 3)
        self.assertEqual(state.cur_hand(), state.hands[0])
        state.submit_play()
        self.assertEqual(state.cur_hand(), state.hands[1])
        state.submit_play()
        self.assertEqual(state.cur_hand(), state.hands[0])

    def test_flip_tile(self):
        """ Test flipping a tile """
        state = gamestate.GameState(2, 8, 3)
        state.hands[0][0] = (6, 0)
        state.flip_tile(0)
        self.assertEqual(state.hands[0][0], (9, 0))
        state.flip_tile(0)
        self.assertEqual(state.hands[0][0], (6, 0))
        state.hands[0][0] = (5, 0)
        state.flip_tile(0)
        self.assertEqual(state.hands[0][0], (5, 0))

    def test_place_tile(self):
        """ Test placing a tile on the board """
        state = gamestate.GameState(2, 8, 3)
        tile = state.hands[0][0]
        state.place_tile(0, 0, 0)
        self.assertEqual(len(state.pending_tiles), 1)
        self.assertEqual(state.pending_tiles[0], (tile[0], tile[1], 0, 0))
        self.assertEqual(len(state.hands[0]), 7)

    def test_remove_tile(self):
        """ Test removing a tile from the board """
        state = gamestate.GameState(2, 8, 3)
        state.place_tile(0, 0, 0)
        self.assertRaises(game.InvalidPlayException, state.remove_tile, 1, 0)
        state.remove_tile(0, 0)
        self.assertEqual(len(state.pending_tiles), 0)
        self.assertEqual(len(state.hands[0]), 8)

    def test_submit_play(self):
        """ Test submitting a play """
        state = gamestate.GameState(2, 8, 3)
        state.hands[0][0] = (3, 0)
        state.place_tile(0, 0, 0)
        state.submit_play()
        self.assertEqual(state.scores[0], 3)
        self.assertEqual(state.player, 1)
        self.assertEqual(len(state.played_tiles), 1)
        self.assertEqual(state.played_tiles[0], (3, 0, 0, 0))
        self.assertEqual(len(state.pending_tiles), 0)
        self.assertEqual(len(state.hands[0]), 8)

        # We complete a line but don't have any tiles left
        state = gamestate.GameState(2, 8, 3)
        state.hands[0] = [(1, 0), (1, 1), (1, 2), (1, 3), (1, 4), (1, 5)]
        state.place_tile(0, 0, 0)
        state.place_tile(0, 0, 1)
        state.place_tile(0, 0, 2)
        state.place_tile(0, 0, 3)
        state.place_tile(0, 0, 4)
        state.place_tile(0, 0, 5)
        state.submit_play()
        self.assertEqual(state.scores[0], 6)
        self.assertEqual(state.player, 1)
        self.assertEqual(len(state.played_tiles), 6)
        self.assertEqual(len(state.pending_tiles), 0)
        self.assertEqual(len(state.hands[0]), 8)

        # We complete a line and have tiles left
        state = gamestate.GameState(2, 8, 3)
        state.hands[0] = [(1, 0), (1, 1), (1, 2), (1, 3), (1, 4), (1, 5),
                          (2, 0)]
        state.place_tile(0, 0, 0)
        state.place_tile(0, 0, 1)
        state.place_tile(0, 0, 2)
        state.place_tile(0, 0, 3)
        state.place_tile(0, 0, 4)
        state.place_tile(0, 0, 5)
        state.submit_play()
        self.assertEqual(state.scores[0], 6)
        self.assertEqual(state.player, 0)
        self.assertEqual(len(state.played_tiles), 6)
        self.assertEqual(len(state.pending_tiles), 0)
        self.assertEqual(len(state.hands[0]), 1)
