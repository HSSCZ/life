import os
from time import sleep

from .helpers import patterns, readCells, wrapX, wrapY, isBit
from .display import LifeDisplay

class Life(object):
    def __init__(self, tickrate, initial_pattern):
        self.display = LifeDisplay()
        self.tickrate = tickrate

        if os.path.exists(initial_pattern):
            pattern = readCells(self.display, initial_pattern)
            self.display.putPattern(pattern)
        elif initial_pattern in patterns.keys():
            self.display.putPattern(patterns[initial_pattern])
        else:
            raise Exception('Pattern does not exist; %s' % initial_pattern)

    def run(self):
       while(1):
            if self.display.isClear():
                sleep(3)
                self.clearDisplay()
                self.display.putPattern(initial_pattern)
                
            os.system('cls' if os.name == 'nt' else 'clear')
            self.display.printDisplay()
            self.lifeStep()
            sleep(1/self.tickrate)

    def neighborCount(self, display, col, bit):
        ''' Check for living cells surrounding a location on the display '''
        count = 0
        for _col in range(-1, 2):
            for _bit in range(-1, 2):
                if _col or _bit:
                    x = wrapX(col, self.display.width, _col)
                    y = wrapY(bit, self.display.height, _bit)
                    if isBit(display()[x], y):
                        count += 1
        return count

    def lifeStep(self):
        tmp_display = list(self.display())

        for col in range(self.display.width):
            for bit in range(1, self.display.height + 1):
                neighbors = self.neighborCount(self.display, col, bit)
                if neighbors == 2:
                    # Cell stays the same
                    pass
                elif neighbors == 3:
                    # Cell lives
                    if not isBit(tmp_display[col], bit):
                        tmp_display[col] |= (1 << (bit - 1))
                else:
                    # Cell dies
                    if isBit(self.display()[col], bit):
                        tmp_display[col] &= ~(1 << (bit - 1))

        self.display.display = tmp_display
