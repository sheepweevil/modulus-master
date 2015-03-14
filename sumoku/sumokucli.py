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


if __name__ == "__main__":
    args = parse_args()
    tiles = sumoku.game.generate_tiles()
    hands = [[] for _ in xrange(args.players)]
    draw_hands(hands, tiles, args.hand_size)

    # Print game state
    print 'Key number: {}'.format(args.key_number)
    for player in xrange(args.players):
        sys.stdout.write("Player {}'s hand: ".format(player + 1))
        for tile in hands[player]:
            output_tile(tile)
        print
