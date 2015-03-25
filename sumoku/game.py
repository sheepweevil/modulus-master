""" Implementation of the sumoku game rules """
import random

# Tile colors
COLOR_RED = 0
COLOR_GREEN = 1
COLOR_YELLOW = 2
COLOR_BLUE = 3
COLOR_MAGENTA = 4
COLOR_CYAN = 5

# Edge of the play space
MIN_X = 0
MAX_X = 51
MIN_Y = 0
MAX_Y = 19

def color_string(color):
    """ Translate a color to a string """
    if color == COLOR_RED:
        return "red"
    if color == COLOR_GREEN:
        return "green"
    if color == COLOR_YELLOW:
        return "yellow"
    if color == COLOR_BLUE:
        return "blue"
    if color == COLOR_MAGENTA:
        return "magenta"
    if color == COLOR_CYAN:
        return "cyan"


def tile_string(tile):
    """ Translate a tile to string """
    return '{} {}'.format(color_string(tile[0]), tile[1])


def played_tile_string(tile):
    """ Translate a played tile to a string """
    return '{} at {},{}'.format(tile_string(tile), tile[2], tile[3])


class InvalidPlayException(Exception):
    """ Exception thrown for an invalid play """
    pass


def score_tiles(tiles, keynumber):
    """ Validates and scores a row or column (collection of tiles) """
    # Just ignore length 1 or 0
    if len(tiles) < 2:
        return 0

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
    return tilesum


def find_tile(x, y, tiles):
    """ Return the tile at position x, y """
    for tile in tiles:
        if tile[2] == x and tile[3] == y:
            return tile
    raise InvalidPlayException('No tile found at {},{}'.format(x, y))


def complete_line(tile, row, tiles):
    """ Complete the line of tiles """
    line = [tile]

    # Search before the start until we can't find any more
    try:
        if row:
            for x in xrange(tile[2] - 1, MIN_X - 1, -1):
                line.append(find_tile(x, tile[3], tiles))
        else:
            for y in xrange(tile[3] - 1, MIN_Y - 1, -1):
                line.append(find_tile(tile[2], y, tiles))
    except InvalidPlayException:
        pass

    # Search after the end until we can't find any more
    try:
        if row:
            for x in xrange(tile[2] + 1, MAX_X + 1):
                line.append(find_tile(x, tile[3], tiles))
        else:
            for y in xrange(tile[3] + 1, MAX_Y + 1):
                line.append(find_tile(tile[2], y, tiles))
    except InvalidPlayException:
        pass

    return line


def score_play(newtiles, tiles, keynumber):
    """ Validates and scores a new play """
    # Special case for skipping turn
    if len(newtiles) == 0:
        return (0, False)

    # Special case for a first play of one tile
    if len(newtiles) == 1 and len(tiles) == 0:
        if newtiles[0][0] % keynumber == 0:
            return (newtiles[0][0], False)
        else:
            raise InvalidPlayException('Sum {} not divisible by {}'
                                       .format(newtiles[0][0], keynumber))

    # Played tiles are tuples (number, color, x, y)
    # Sort the tiles to make things easier
    newtiles.sort()

    # Make sure the new tiles are all in the same row or column
    row = newtiles[0][3]
    col = newtiles[0][2]
    notrow = False
    notcol = False
    for tile in newtiles[1:]:
        if tile[3] != row:
            notrow = True
        if tile[2] != col:
            notcol = True
        if notrow and notcol:
            raise InvalidPlayException('Tiles not in a single row or column')

    alltiles = list(newtiles)
    alltiles.extend(tiles)

    # Score the major axis once, and minor axis for each new tile
    completed = False
    mainline = complete_line(newtiles[0], notcol, alltiles)
    if newtiles[-1] not in mainline:
        raise InvalidPlayException('Gaps in main line')
    if len(mainline) == 6:
        completed = True

    score = score_tiles(mainline, keynumber)
    for tile in newtiles:
        line = complete_line(tile, not notcol, alltiles)
        if len(line) == 6:
            completed = True
        score = score + score_tiles(line, keynumber)
    return (score, completed)


def get_key_number():
    """ Determine a random key number """
    return random.randrange(3, 6)


def generate_tiles():
    """ Generates the tiles to start the game """
    tiles = []
    for num in xrange(1, 9):
        for color in xrange(0, 6):
            tiles.append((num, color))
            tiles.append((num, color))
    return tiles


def draw_tile(tiles):
    """ Draw a random tile from the remaining ones """
    tile = random.choice(tiles)
    tiles.remove(tile)
    return tile
