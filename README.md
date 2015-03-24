# Modulus Master

Modulus Master is an implementation of the rules of Sumoku (TM)
by Blue Orange Games.

## Rules

The objective is to score the most number of points by placing
new tiles in a single row or column such that the sum of each
line is divisible by the key number. In addition, colors cannot
be repeated within a line (but numbers can).

## Playing

To run the command line client, use a terminal at least 80
characters wide and 24 lines tall, which supports ANSI
escape codes. Set your `PYTHONPATH` to include the project
top level directory, and run `sumokucli.py`.

```
usage: sumokucli.py [-h] [--players {2,3,4,5}] [--key-number {3,4,5,random}]
                    [--hand-size HAND_SIZE]

A command line sumoku game

optional arguments:
  -h, --help            show this help message and exit
  --players {2,3,4,5}   number of players
  --key-number {3,4,5,random}
                        key number, or 'random'
  --hand-size HAND_SIZE
                        number of tiles in hand
```

Players interact with the game by entering commands.
For commands, columns are identified by letters, rows
and tiles by number.

```
help,?                   Print this help message
submit                   Submit the current play
flip <tile>              Flip a tile between 6 and 9
place <tile> <col> <row> Place a tile on the board
remove <col> <row>       Remove a tile from the board
```
