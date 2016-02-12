'''
life.py - Conway's Game of Life in a terminal

The game board is stored as a list of numbers with the each bit of the
numbers representing a cell.  Board wraps around on the edges.
    
The x axis is the index in to the array, y axis is a bit position
'''
import os
import sys
from time import sleep

from life import LifeDisplay

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

    if len(cells) >= display.height:
        raise Exception('Pattern taller than board')
    elif len(cells[0]) >= display.width:
        raise Exception('Pattern wider than board')

    cells = list(zip(*cells))
    c_ints = [0 for x in range(len(cells))]

    for i, row in enumerate(cells):
        for j, val in enumerate(row):
            if val == 'O':
                c_ints[i] |= 1 << j

    display.putPattern(c_ints)

def wrapX(x, limit, add):
    ''' Add to x index, wrapping around from limit to 0 '''
    new = x + add
    while new < 0:
        new += limit
    while new >=  limit:
        new -= limit
    return new

def wrapY(y, limit, add):
    ''' Add to y index (a bit location), wrapping around from limit to 1 '''
    new = y + add
    while new < 1:
        new += limit  
    while new > limit:
        new -= limit
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
                nx = wrapX(col, display.width, _col)
                ny = wrapY(bit, display.height, _bit)
                if isBit(display()[nx], ny):
                    count += 1
    return count

def lifeStep(display):
    tmp_display = list(display())

    for col in range(display.width):
        for bit in range(1, display.height + 1):
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
        
def doStuff(display, pattern):
    ''' If pattern exists then put it on the board '''
    if os.path.exists(pattern):
        readCells(display, pattern)
    elif pattern in patterns.keys():
        display.putPattern(patterns[pattern])
    else:
        raise Exception('Pattern does not exist: %s' % pattern)

def main(argv):
    # print('w: %d, h: %d' % (WIDTH, BIT_LIMIT))
    screen = LifeDisplay()
    doStuff(screen, argv[1])

    while(1):
        # If all cells have died then wait a bit then reset the board
        if screen.isClear():
            sleep(10)
            doStuff(screen)
            
        os.system('cls' if os.name == 'nt' else 'clear')
        screen.printDisplay()
        screen.display = lifeStep(screen)
        sleep(1/16)

def usage():
    print('Usage: python3 life.py [pattern]')
    print('[pattern] is a built-in pattern or the path to a cells file')

if __name__ == '__main__':
    if len(sys.argv) != 2:
        print('Invalid argument')
        usage()
        exit(1)
    main(sys.argv)
