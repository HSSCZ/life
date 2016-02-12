'''
life.py - Conway's Game of Life in a terminal

The game board is stored as a list of numbers with the each bit of the
numbers representing a cell.  Board wraps around on the edges.
    
The x axis is the index in to the array, y axis is a bit position
'''
import os
import sys
import shutil 
from time import sleep

# Fit game board in the current terminal
term_size = shutil.get_terminal_size()

WIDTH = term_size.columns // 2
# Bits 1 through BIT_LIMIT are used as rows of a grid
if os.name == 'nt':
    BIT_LIMIT = term_size.lines // 3
else:
    BIT_LIMIT = term_size.lines // 2

# A few built in cell patterns
patterns = {
    'glider': [0x20, 0x10, 0x70],
    'looper': [0x20, 0x60, 0x20],
    'lwss': [0x38, 0x24, 0x20, 0x20, 0x14],
    'oscillate': [0x38],
    'puffer2': [0x20, 0x40, 0x44, 0x78,
                0x0, 0x0, 0x0,
                0x04, 0x18, 0x10, 0x10, 0x08,
                0x0, 0x0,
                0x20, 0x40, 0x44, 0x78],
    'R-pentomino': [0x40, 0xe0, 0x80]
    }

def readCells(display, path):
    ''' Read a cell pattern from the file at path and put it on the display '''
    if os.path.exists(path):
        with open(path) as f:
            cells = f.readlines()[2:]

    if len(cells) >= BIT_LIMIT:
        raise Exception('Pattern taller than board')
    elif len(cells[0]) >= WIDTH:
        raise Exception('Pattern wider than board')

    cells = list(zip(*cells))
    c_ints = [0 for x in range(len(cells))]

    for i, row in enumerate(cells):
        for j, val in enumerate(row):
            if val == 'O':
                c_ints[i] |= 1 << j

    putPattern(display, c_ints)

def wrapX(x, add):
    ''' Add to x index, wrapping around from WIDTH to 0 '''
    new = x + add
    while new < 0:
        new += WIDTH
    while new >= WIDTH:
        new -= WIDTH
    return new

def wrapY(y, add):
    ''' Add to y index (a bit location), wrapping around from BIT_LIMIT to 1 '''
    new = y + add
    while new < 1:
        new += BIT_LIMIT 
    while new > BIT_LIMIT:
        new -= BIT_LIMIT
    return new

def isBit(n, bit):
    if (n & (1 << (bit - 1))):
        return True
    return False
    
def neighborCount(display, col, bit):
    ''' Check bits surrounding bit in display for set bits '''
    count = 0
    for _col in range(-1, 2):
        for _bit in range(-1, 2):
            if _col or _bit:
                if isBit(display[wrapX(col, _col)], wrapY(bit, _bit)):
                    count += 1
    return count

def lifeStep(display):
    tmp_display = list(display)

    for col in range(len(display)):
        for bit in range(1, BIT_LIMIT + 1):
            neighbors = neighborCount(display, col, bit)
            if neighbors == 2:
                # Cell stays the same
                pass
            elif neighbors == 3:
                # Cell lives
                if not isBit(tmp_display[col], bit):
                    tmp_display[col] |= (1 << (bit - 1))
            else:
                # Cell dies
                if isBit(tmp_display[col], bit):
                    tmp_display[col] &= ~(1 << (bit - 1))

    return tmp_display

def printDisplay(display):
    for bit in range(0, BIT_LIMIT):
        for i in range(WIDTH):
            alive = bool(display[i] & (1 << bit))
            print('%2s' % '#' if alive else '  ', end='')
        print('\n')

def putPattern(display, pattern):
    ''' Put pattern on the display '''
    shift_pos = (WIDTH // 2) - (len(pattern) // 2)

    for i, v in enumerate(pattern):
        display[i+shift_pos] = v
        
def doStuff(display, pattern=None):
    ''' If pattern exists then put it on the board '''
    if os.path.exists(pattern):
        readCells(display, pattern)
    elif pattern in patterns.keys():
        putPattern(display, patterns[pattern])
    else:
        raise Exception('Pattern does not exist: %s' % pattern)
        
def main(argv):
    # print('w: %d, h: %d' % (WIDTH, BIT_LIMIT))
    display = [0 for x in range(WIDTH)]
    doStuff(display, argv[1])

    while(1):
        # If all cells have died then wait a bit then reset the board
        if sum(display) == 0:
            sleep(10)
            doStuff(display)
            
        os.system('cls' if os.name == 'nt' else 'clear')
        printDisplay(display)
        display = lifeStep(display)
        sleep(1/4)

def usage():
    print('Usage: python3 life.py [pattern]')
    print('[pattern] is a built-in pattern or the path to a cells file')

if __name__ == '__main__':
    if len(sys.argv) != 2:
        print('Invalid argument')
        usage()
        exit(1)
    main(sys.argv)
