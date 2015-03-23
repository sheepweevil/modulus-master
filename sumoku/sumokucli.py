#!/usr/bin/env python
""" A CLI interface to play sumoku """
import argparse
import sumoku.game
import sumoku.gamestate


class IllegalCommandException(Exception):
    """ Exception raised for badly formatted commands """
    pass


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
    return tile


def parse_col(colstr):
    """ Parse a column from user input """
    if len(colstr) != 1:
        raise IllegalCommandException('Column must be a-zA-Z')

    colnum = ord(colstr)
    if colnum >= ord('a'):
        colnum = colnum - ord('a')
    else:
        colnum = colnum - ord('A') + 26
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


def handle_command(state):
    """ Get a command from the user and perform appropriate action """
    command = raw_input('Player {} enter command (? for help): '
                        .format(state.player + 1)).split()
    hand = state.cur_hand()

    if len(command) == 0:
        command_help()
    elif command[0] == 'submit':
        state.submit_play()
    elif command[0] == 'flip':
        if len(command) != 2:
            raise IllegalCommandException('Flip command takes one argument')

        tile = parse_tile(command[1], hand)
        state.flip_tile(tile)
    elif command[0] == 'place':
        if len(command) != 4:
            raise IllegalCommandException('Place command takes 3 arguments')

        tile = parse_tile(command[1], hand)
        col = parse_col(command[2])
        row = parse_row(command[3])
        state.place_tile(tile, col, row)
    elif command[0] == 'remove':
        if len(command) != 3:
            raise IllegalCommandException('Remove command takes 2 arguments')

        col = parse_col(command[1])
        row = parse_row(command[2])
        state.remove_tile(col, row)
    else:
        command_help()
    return False


def play_sumoku():
    """ Play a game of sumoku """
    args = parse_args()
    state = sumoku.gamestate.GameState(args.players, args.hand_size,
                                       args.key_number)

    state.print_game()
    while True:
        try:
            handle_command(state)
            state.print_game()
        except IllegalCommandException, err:
            print 'Error: {}'.format(err.message)


if __name__ == "__main__":
    play_sumoku()
