#!/usr/bin/env python
""" A CLI interface to play sumoku """
import argparse
import sumoku.game
import sys


class IllegalCommandException(Exception):
    """ Exception raised for badly formatted commands """
    pass


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
    """ Print the game state """

    print '   abcdefghijklmnopqrstuvwxyzABCDEFGHIJKLMNOPQRSTUVWXYZ'
    for y in xrange(sumoku.game.MIN_Y, sumoku.game.MAX_Y + 1):
        sys.stdout.write('{:2} '.format(y + 1))
        for x in xrange(sumoku.game.MIN_X, sumoku.game.MAX_X + 1):
            try:
                output_tile(sumoku.game.find_tile(x, y, played_tiles))
            except sumoku.game.InvalidPlayException:
                sys.stdout.write('-')

        if y == 0:
            print ' Key number: {}'.format(args.key_number)
        elif y == 1:
            print ' Tiles remaining: {}'.format(len(tiles))
        elif y - 3 >= 0 and y - 3 < args.players:
            player = y - 3
            sys.stdout.write(' P{} Score: {:04} Hand: '
                             .format(player + 1, scores[player]))
            for tile in hands[player]:
                output_tile(tile)
            print
        else:
            print


def command_help():
    """ Print help for commands """
    print 'help,?                   Print this help message'
    print 'submit                   Submit the current play'
    print 'flip <tile>              Flip a tile between 6 and 9'
    print 'place <tile> <col> <row> Place a tile on the board'
    print 'remove <col> <row>       Remove a tile from the board'


def parse_tile(tilestr, hand):
    """ Parse a tile from user input """
    tile = int(tilestr) - 1
    if tile < 0 or tile >= len(hand):
        raise IllegalCommandException('Tile must be between {} and {}'
                                      .format(1, len(hand)))
    return hand[tile]


def parse_col(colstr):
    """ Parse a column from user input """
    if len(colstr) != 1:
        raise IllegalCommandException('Column must be a-zA-Z')

    colnum = ord(colstr)
    if colnum > ord('a'):
        colnum = colnum - ord('a') + 26
    else:
        colnum = colnum - ord('A')
    if colnum < 0 or colnum > sumoku.game.MAX_X:
        raise IllegalCommandException('Column must be a-zA-Z')
    return colnum


def parse_row(rowstr):
    """ Parse a row from user input """
    row = int(rowstr) - 1
    if row < 0 or row > sumoku.game.MAX_Y:
        raise IllegalCommandException('Row must be 1-{}'
                                      .format(sumoku.game.MAX_Y + 1))
    return row


def handle_command(player, hand):
    """ Get a command from the user and perform appropriate action """
    command = raw_input('Player {} enter command (? for help): '
                        .format(player + 1)).split()

    if len(command) == 0:
        command_help()
    elif command[0] == 'submit':
        return True
    elif command[0] == 'flip':
        if len(command) != 2:
            raise IllegalCommandException('Flip command takes one argument')

        tile = parse_tile(command[1], hand)
    elif command[0] == 'place':
        if len(command) != 4:
            raise IllegalCommandException('Place command takes 3 arguments')

        tile = parse_tile(command[1], hand)
        row = parse_row(command[2])
        col = parse_col(command[3])
    elif command[0] == 'remove':
        if len(command) != 3:
            raise IllegalCommandException('Remove command takes 2 arguments')

        row = parse_row(command[1])
        col = parse_col(command[2])
    else:
        command_help()
    return False


def play_sumoku():
    """ Play a game of sumoku """
    args = parse_args()
    tiles = sumoku.game.generate_tiles()
    hands = [[] for _ in xrange(args.players)]
    draw_hands(hands, tiles, args.hand_size)
    scores = [0 for _ in xrange(args.players)]
    played_tiles = []

    print_game(args, hands, scores, tiles, played_tiles)
    turn_done = False
    while not turn_done:
        turn_done = handle_command(0, hands[0])


if __name__ == "__main__":
    play_sumoku()
