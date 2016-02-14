# life.py

Conway's Game of Life in a terminal

Usage: `life.py [pattern]` where `[pattern]` is a built-in pattern
(in life.helpers.patterns) or the name of a file in the `cells` folder

The game has a few controls:
    `.`: increase tickrate
    `,`: decrease tickrate
    `p`: pause
    `s`: (when paused) step forward once
    `r`: resume
    `q`: quit

The game board is stored as a list of ints.  Each int is a column of the board.
An `on` bit in an int represents a living cell.

Game board is sized to fit the current terminal.  Run in a fullscreen terminal
for the best view and ability to use larger initial patterns.

More cells files available at: http://www.bitstorm.org/gameoflife/lexicon/
