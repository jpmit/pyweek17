#! /usr/bin/env python

from gamelib import game, menu

if __name__ == '__main__':
    gm = game.Game()
    mn = menu.Menu(gm)
    while True:
        # start menu
        levsel, single = mn.start()

        # play game
        gm.main(levsel, single)

        # finish sequence
        mn.finish()
