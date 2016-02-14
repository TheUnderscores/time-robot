#!/usr/bin/env python3
import sdl2
import sdl2.ext

sdl2.ext.init()

import game
g = game.Game()
g.startGame()

sdl2.ext.quit()
