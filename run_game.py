#! /usr/bin/env python

from gamelib import game, menu

if __name__ == '__main__':
    gm = game.Game()
    mn = menu.Menu(gm)
    while True:
        # start menu
        mn.start()

        # play game
        gm.main()

        # finish sequence
        mn.finish()
