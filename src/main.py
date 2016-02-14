#!/usr/bin/env python3
import sdl2
import sdl2.ext

import sys

if len(sys.argv) < 3:
    print("Run with main.py <level file> <code file>")
    sys.exit(-1)

level_file = sys.argv[1]
code_file = sys.argv[2]

sdl2.ext.init()

import game
g = game.Game()
g.startGame(level_file, code_file)

sdl2.ext.quit()
