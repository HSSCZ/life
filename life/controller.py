import os
import time
from time import sleep

if os.name == 'nt':
    from .helpers import write_ms32

from .helpers import patterns, readCells, wrapX, wrapY, isBit, getch
from .display import LifeDisplay

class Life(object):
    def __init__(self, tickrate, initial_pattern, cell_symbol, cell_color):
        '''
        Args:
        tickrate: game updates per second
        initial_pattern: an item from helpers.patterns or path to cells file
        cell_symbol: a character to represent cells
        cell_color: BASH color code
        '''
        self.display = LifeDisplay(cell_symbol, cell_color)
        self.tickrate = tickrate
        self.state = 'running'
        self.steps = 0
        self.show_stats = False

        if os.path.exists(initial_pattern):
            pattern = readCells(initial_pattern)
            self.display.putPattern(pattern)
        elif initial_pattern in patterns.keys():
            self.display.putPattern(patterns[initial_pattern])
        else:
            raise Exception('Pattern does not exist; {}'.format(initial_pattern))

    def run(self):
        ''' Main loop '''
        while(1):
            if self.state == 'running':
                last_time = time.time()
                while (1):
                    if self.state != 'running':
                        break
                    if self.display.isClear():
                        sleep(3)
                        self.display.clearDisplay()
                        self.display.putPattern(patterns['lwss'])

                    cur_time = time.time()
                    if cur_time - last_time >= 1/self.tickrate:
                        self.printGame()
                        self.lifeStep()
                        last_time = time.time()
                    self.checkInput()

            elif self.state == 'paused':
                self.printGame()
                while(1):
                    if self.state != 'paused':
                        break
                    if self.checkInput():
                        self.printGame()

            else:
                raise Exception('Invalid state: {}'.format(self.state))

    def quit(self):
        ''' Make sure terminal is in normal mode, clear it, and exit '''
        if os.name == 'posix':
            os.system('stty sane')
        os.system('cls' if os.name == 'nt' else 'clear')
        exit(0)

    def pause(self):
        ''' Pause updating '''
        self.state = 'paused'

    def resume(self):
        ''' Resume updating '''
        self.state = 'running'

    def printGame(self):
        self.display.printDisplay()
        if self.show_stats:
            self._printStats()

    def _printStats(self):
        ''' Print some stats on top of the display '''
        w = self.display.width
        h = self.display.height
        p = self.steps
        t = self.tickrate
        s = self.state
        stats = ('\x1b[0;0f' # print at 0,0
                 'w:{}\n'
                 'h:{}\n'
                 'steps:{}\n'
                 'tickrate:{}\n'
                 '{}'.format(w,h,p,t,s))

        if os.name == 'nt':
            write_ms32(stats[6:], 0, 0)
        else:
            print(stats)

    def checkInput(self):
        c = getch()

        if c == 'p':
            self.pause()
        elif c == 'q':
            self.quit()
        elif c == 'r':
            self.resume()
        elif c == 's':
            if self.state == 'paused':
                self.lifeStep()
        elif c == 't':
            self.show_stats = not self.show_stats
        elif c == '.':
            if self.tickrate == 1:
                self.tickrate = 4
            else:
                self.tickrate += 4
            if self.tickrate > 36:
                self.tickrate = 36
        elif c == ',':
            self.tickrate -= 4
            if self.tickrate <= 0:
                self.tickrate = 1
        else:
            return False
        return True

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
        ''' Compute a step in life and update the display '''
        tmp_display = list(self.display())

        for col in range(self.display.width):
            # If previous, current, and next column are empty then we don't
            # need to do anything
            if (self.display()[col] == 0
                and self.display()[wrapX(col, self.display.width, -1)] == 0
                and self.display()[wrapX(col, self.display.width,  1)] == 0):
                continue

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

        self.steps += 1
        self.display.display = tmp_display
