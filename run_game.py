#! /usr/bin/env python

from gamelib import game, menu

if __name__ == '__main__':
    gm = game.Game()
    mn = menu.Menu(gm)
    while True:
        # start menu
        levsel = mn.start()

        # play game
        gm.main(levsel)

        # finish sequence
        mn.finish()
