import os
import shutil

class LifeDisplay(object):
    '''
    LifeDisplay is a list of numbers with each bit of a number representing a cell

    The x axis is the index in to the array, y axis is a bit position
    '''
    def __init__(self):
        term_size = shutil.get_terminal_size()

        self.width = term_size.columns // 2

        if os.name == 'nt':
            self.height = term_size.lines // 3
        else:
            self.height = term_size.lines // 2

        self.display = [0 for x in range(self.width)]

    def __call__(self):
        return self.display

    def putPattern(self, pattern):
        if len(pattern) >= self.width:
            raise Exception('Pattern wider than board')
        elif max(pattern) > 1 << self.height:
            raise Exception('Pattern taller than board')

        # get the center of the display
        horz_pos = (self.width // 2) - (len(pattern) // 2)
        vert_pos = (self.height // 2) - ((len(bin(max(pattern))) - 2) // 2)

        for i, v in enumerate(pattern):
            self.display[i+horz_pos] = v << vert_pos

    def clearDisplay(self):
        self.display = [0 for x in range(self.width)]

    def printDisplay(self):
        for bit in range(0, self.height):
            for i in range(self.width):
                alive = bool(self.display[i] & (1 << bit))
                print('%2s' % '#' if alive else '  ', end='')
            print('\n')

    def isClear(self):
        return False if sum(self()) else True
