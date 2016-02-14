import os
from time import sleep

from .helpers import patterns, readCells, wrapX, wrapY, isBit, getch
from .display import LifeDisplay

class Life(object):
    def __init__(self, tickrate, initial_pattern):
        '''
        Args:
        tickrate: game updates per second
        initial_pattern: an item from helpers.patterns or path to cells file
        '''
        self.display = LifeDisplay()
        self.tickrate = tickrate
        self.state = 'running'

        if os.path.exists(initial_pattern):
            pattern = readCells(self.display, initial_pattern)
            self.display.putPattern(pattern)
        elif initial_pattern in patterns.keys():
            self.display.putPattern(patterns[initial_pattern])
        else:
            raise Exception('Pattern does not exist; %s' % initial_pattern)

    def run(self):
        ''' Main loop '''
        while(1):
            if self.state == 'running':
                while (1):
                    if self.state != 'running':
                        break
                    if self.display.isClear():
                        sleep(3)
                        self.clearDisplay()
                        self.display.putPattern(initial_pattern)

                    self.display.printDisplay()
                    self.lifeStep()
                    self.checkInput()
                    sleep(1/self.tickrate)

            elif self.state == 'paused':
                self.display.printDisplay()
                print('Life paused . . .')
                while(1):
                    if self.state != 'paused':
                        break
                    self.checkInput()

            else:
                raise Exception('Invalid state: %s' % self.state)

    def quit(self):
        ''' Make sure terminal is in normal mode and exit '''
        if os.name == 'posix':
            os.system('stty sane')
        exit(0)

    def pause(self):
        ''' Pause updating '''
        self.state = 'paused'

    def resume(self):
        ''' Resume updating '''
        self.state = 'running'

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
                self.display.printDisplay()
                print('Life paused . . .')
        elif c == '.':
            if self.tickrate == 1:
                self.tickrate = 4
            else:
                self.tickrate += 4
        elif c == ',':
            self.tickrate -= 4
            if self.tickrate <= 0:
                self.tickrate = 1

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
