import os
import shutil

class LifeDisplay(object):
    '''
    LifeDisplay is a list of numbers with each bit of a number representing a cell

    The x axis is the index in to the array, y axis is a bit position
    '''
    def __init__(self, cell_symbol, cell_color):
        '''
        Args:
        cell_symbol: a character to represent cells
        cell_color: BASH color code
        '''
        term_size = shutil.get_terminal_size()

        # divided by two because cells are printed two wide
        # ie ' #' for a live cell
        self.width = term_size.columns // 2

        if os.name == 'nt':
            # cmd and powershell have double spaced lines or something
            # divide by 2 or the game isn't displayed right
            self.height = term_size.lines // 2
        else:
            self.height = term_size.lines

        self.display = [0 for x in range(self.width)]
        # don't bother dealing with unicode and colors on Windows
        # Windows gets default cell symbol
        self.cell_symbol = cell_symbol if os.name == 'posix' else '▒'
        self.cell_color = cell_color if os.name == 'posix' else ''

    def __call__(self):
        return self.display

    def putPattern(self, pattern):
        ''' Put pattern on the center of the display '''
        if len(pattern) >= self.width:
            raise Exception('Pattern wider than display')
        elif max(pattern) > 1 << self.height:
            raise Exception('Pattern taller than display')

        # get the center of the display
        horz_pos = (self.width // 2) - (len(pattern) // 2)
        vert_pos = (self.height // 2) - (len(bin(max(pattern))[2:]) // 2)

        for i, v in enumerate(pattern):
            self.display[i+horz_pos] = v << vert_pos

    def clearDisplay(self):
        self.display = [0 for x in range(self.width)]

    def printDisplay(self):
        ''' Clear the screen and print the display '''
        os.system('cls' if os.name == 'nt' else 'clear')

        display_string = '{}'.format(self.cell_color)
        for bit in range(0, self.height):
            w_string = ''
            for i in range(self.width):
                alive = bool(self.display[i] & (1 << bit))
                w_string += '{:>2.2}'.format(self.cell_symbol if alive else '  ')
            display_string += w_string + '\n'
        display_string += '' if os.name == 'nt' else '\x1b[0m'
        print(display_string)

    def isClear(self):
        return False if sum(self()) else True
