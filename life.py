#!/usr/bin/env python3
'''
life.py - Conway's Game of Life in a terminal
'''
import sys

from life import Life
        
def usage():
    print('Usage: life.py [pattern]')
    print('[pattern] is a built-in pattern or the path to a cells file')

if __name__ == '__main__':
    if len(sys.argv) != 2:
        print('Invalid argument')
        usage()
        exit(1)

    cell_symbol = '\u2b1b\u2b2f'
    cell_color = '\x1b[38;5;9m'

    Life(8, sys.argv[1], cell_symbol, cell_color).run()
