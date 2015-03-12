""" Implementation of the sumoku game rules """
import random

# Tile colors
COLOR_RED = 0
COLOR_ORANGE = 1
COLOR_YELLOW = 2
COLOR_GREEN = 3
COLOR_BLUE = 4
COLOR_PURPLE = 5


def color_string(color):
    """ Translate a color to a string """
    if color == COLOR_RED:
        return "red"
    if color == COLOR_ORANGE:
        return "orange"
    if color == COLOR_YELLOW:
        return "yellow"
    if color == COLOR_GREEN:
        return "green"
    if color == COLOR_BLUE:
        return "blue"
    if color == COLOR_PURPLE:
        return "purple"


class InvalidPlayException(Exception):
    """ Exception thrown for an invalid play """
    pass


def validate_play(tiles, keynumber):
    """ Validates a row or column (collection of tiles) """
    # Check that sum is divisible by the key number
    tilesum = sum([tile[0] for tile in tiles])
    if tilesum % keynumber != 0:
        raise InvalidPlayException('Sum {} not divisible by {}'
                                   .format(tilesum, keynumber))

    # Check that no colors are repeated
    colors = []
    for tile in tiles:
        color = tile[1]
        if color in colors:
            raise InvalidPlayException('Color {} used more than once'
                                       .format(color_string(color)))
        colors.append(color)
    return True


def get_key_number():
    """ Determine a random key number """
    return random.randrange(3, 6)


def draw_tile(tiles):
    """ Draw a random tile from the remaining ones """
    tile = random.choice(tiles)
    tiles.remove(tile)
    return tile
