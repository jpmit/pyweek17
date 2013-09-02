import pygame
import const
import data
import sys
import pygame
import powerbar, rocket, moon, gravitybar
import level
#from pygame.locals import * # remove this later

class Game(object):
    def __init__(self):

        pygame.init()

        # set up screen etc.
        self.screen = pygame.display.set_mode(const.DMODE)
        self.swidth = self.screen.get_width()
        self.sheight = self.screen.get_height()        

        # for getting right FPS
        self.clock = pygame.time.Clock()

        # background
        background = pygame.image.load(data.filepath('ghettoville2.jpg'\
                                                     )).convert_alpha()
        self.background = pygame.transform.scale(background, const.DMODE)
        # black background for now
        #self.background = pygame.Surface(const.DMODE)

        self.store_globals()

    def store_globals(self):
        """We store references to some things here that are needed all
        over the game."""

        # the main sprites
        self.moon = moon.Moon()
        self.rocket = rocket.Rocket()
        self.pbar = powerbar.Powerbar()
        self.gbar = gravitybar.Gravitybar()

        # some states needed by many objects
        self.hitmoon = False
        self.rktdead = False # dead if gone off-screen
        self.hitasteroid = False

    def main(self):
        for levnum in [0, 1]:
            nextlevel = level.Level(self, levnum)
            nextlevel.main()
        pygame.quit()
        #sys.exit()

if __name__ == '__main__':
    gm = Game()
    gm.main()
