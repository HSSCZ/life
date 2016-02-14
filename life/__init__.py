'''
Conway's Game of Life

controller.py contains the Life class which implements Conway's Game of Life as
a terminal program.

The game board is stored as a list of ints.  Each int is a column of the board.
An `on` bit in an int represents a living cell.

Game board is sized to fit the current terminal.  Run in a fullscreen terminal
for the best view and ability to use larger initial patterns.
'''
from .controller import Life
