""" A class holding game state """
import sumoku.game
import sys


def output_tile(tile, highlight):
    """ Print a tile in color """
    sys.stdout.write('\x1b[{};{}1m{}\x1b[0m'
                     .format(31 + tile[1], '47;' if highlight else '',
                             tile[0]))


class GameState(object):
    """ A class holding sumoku game state """

    def __init__(self, players, hand_size, key_number):
        """ Construct the game state from initial parameters """
        self.players = players
        self.hand_size = hand_size
        self.key_number = key_number
        self.tiles = sumoku.game.generate_tiles()
        self.hands = [[] for _ in xrange(players)]
        self.draw_tiles()
        self.scores = [0 for _ in xrange(players)]
        self.played_tiles = []
        self.pending_tiles = []
        self.player = 0

    def draw_tiles(self):
        """ Draw tiles to fill up hands """
        for hand in self.hands:
            while len(hand) < self.hand_size and len(self.tiles) > 0:
                hand.append(sumoku.game.draw_tile(self.tiles))
            hand.sort()

    def cur_hand(self):
        """ Return the hand of the current player """
        return self.hands[self.player]

    def flip_tile(self, tile):
        """ Flip a tile between 6 and 9 """
        hand = self.cur_hand()
        if hand[tile][0] == 6:
            hand[tile] = (9, hand[tile][1])
        elif hand[tile][0] == 9:
            hand[tile] = (6, hand[tile][1])

    def place_tile(self, tile, col, row):
        """ Place a tile on the board """
        hand = self.cur_hand()
        self.pending_tiles.append((hand[tile][0], hand[tile][1], col, row))
        del hand[tile]

    def remove_tile(self, col, row):
        """ Remove a tile from the board """
        tile = sumoku.game.find_tile(col, row, self.pending_tiles)
        self.pending_tiles.remove(tile)
        self.cur_hand().append((tile[0], tile[1]))

    def submit_play(self):
        """ Submit a play """
        self.scores[self.player] = (self.scores[self.player] +
                                    sumoku.game.score_play(self.pending_tiles,
                                                           self.played_tiles,
                                                           self.key_number))
        self.player = (self.player + 1) % self.players
        self.played_tiles.extend(self.pending_tiles)
        self.pending_tiles = []
        self.draw_tiles()

    def print_game(self):
        """ Print the game state """
        print '   abcdefghijklmnopqrstuvwxyzABCDEFGHIJKLMNOPQRSTUVWXYZ'
        for row in xrange(sumoku.game.MIN_Y, sumoku.game.MAX_Y + 1):
            sys.stdout.write('{:2} '.format(row + 1))
            for col in xrange(sumoku.game.MIN_X, sumoku.game.MAX_X + 1):
                try:
                    tile = sumoku.game.find_tile(col, row, self.played_tiles)
                    output_tile(tile, False)
                except sumoku.game.InvalidPlayException:
                    try:
                        tile = sumoku.game.find_tile(col, row,
                                                     self.pending_tiles)
                        output_tile(tile, True)
                    except sumoku.game.InvalidPlayException:
                        sys.stdout.write('-')

            if row == 0:
                print ' Key number: {}'.format(self.key_number)
            elif row == 1:
                print ' Tiles remaining: {}'.format(len(self.tiles))
            elif row == 3:
                print ' Player Score Hand'
            elif row == 4:
                print '              12345678'
            elif row - 5 >= 0 and row - 5 < self.players:
                player = row - 5
                sys.stdout.write(' ')
                if player == self.player:
                    sys.stdout.write('\x1b[47m')
                sys.stdout.write('{:6} {:05} '
                                 .format(player + 1, self.scores[player]))
                for tile in self.hands[player]:
                    output_tile(tile, player == self.player)
                print
            else:
                print
