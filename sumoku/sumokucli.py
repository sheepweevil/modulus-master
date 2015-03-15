#!/usr/bin/env python
""" A CLI interface to play sumoku """
import argparse
import sumoku.game
import sys


def output_tile(tile):
    """ Print a tile in color """
    sys.stdout.write('\x1b[{};1m{}\x1b[0m'.format(31 + tile[1], tile[0]))


def parse_args():
    """ Parse command line arguments """
    parser = argparse.ArgumentParser(description='A command line sumoku game')
    parser.add_argument('--players', default=2, type=int,
                        choices=range(2, 6), help='number of players')
    parser.add_argument('--key-number', default='random',
                        choices=['3', '4', '5', 'random'],
                        help="key number, or 'random'")
    parser.add_argument('--hand-size', default=8, type=int,
                        help='number of tiles in hand')

    args = parser.parse_args()

    # Get key number
    if args.key_number == "random":
        args.key_number = sumoku.game.get_key_number()
    else:
        args.key_number = int(args.key_number)

    return args


def draw_hands(hands, tiles, hand_size):
    """ Draw hands for each player """
    for hand in hands:
        while len(hand) < hand_size and len(tiles) > 0:
            hand.append(sumoku.game.draw_tile(tiles))
        hand.sort()


def print_game(args, hands, scores, tiles, played_tiles):
    print 'Key number: {} Tiles remaining: {}'.format(args.key_number, len(tiles))
    for player in xrange(args.players):
        sys.stdout.write("Player {}'s Score: {:4} Hand: ".format(player + 1, scores[player]))
        for tile in hands[player]:
            output_tile(tile)
        print

    print '   abcdefghijklmnopqrstuvwxyzABCDEFGHIJKLMNOPQRSTUVWXYZ'
    for y in xrange(sumoku.game.MIN_Y, sumoku.game.MAX_Y + 1):
        sys.stdout.write('{:2} '.format(y + 1))
        for x in xrange(sumoku.game.MIN_X, sumoku.game.MAX_X + 1):
            try:
                output_tile(sumoku.game.find_tile(x, y, played_tiles))
            except sumoku.game.InvalidPlayException:
                sys.stdout.write('-')
        print


def command_help():
    print 'help,?                   Print this help message'
    print 'submit                   Submit the current play'
    print 'flip <tile>              Flip a tile between 6 and 9'
    print 'place <tile> <col> <row> Place a tile on the board'
    print 'remove <col> <row>       Remove a tile from the board'


def handle_command(player):
    command = raw_input('Player {} enter command (? for help): '
                        .format(player))
    command_args = command.split()


if __name__ == "__main__":
    args = parse_args()
    tiles = sumoku.game.generate_tiles()
    hands = [[] for _ in xrange(args.players)]
    draw_hands(hands, tiles, args.hand_size)
    scores = [0 for _ in xrange(args.players)]
    played_tiles = []

    print_game(args, hands, scores, tiles, played_tiles)
    handle_command(0)
    command_help()
