import os

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
    ''' Read a cell pattern from the file at path
        Return the pattern as an int array

        Args:
        display: LifeDisplay object
        path: path to cells file
    '''
    if os.path.exists(path):
        with open(path) as f:
            cells = f.readlines()[2:]

    # build int array from file
    cells = list(zip(*cells))
    c_ints = [0 for x in range(len(cells))]

    for i, row in enumerate(cells):
        for j, val in enumerate(row):
            if val == 'O':
                c_ints[i] |= 1 << j

    return c_ints

def wrapX(x, limit, add):
    ''' Add to x, wrapping around from limit to 0 '''
    new = x + add
    while new < 0:
        new += limit
    while new >=  limit:
        new -= limit
    return new

def wrapY(y, limit, add):
    ''' Add to y (a bit location), wrapping around from limit to 1 '''
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