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
        #self.background = pygame.transform.scale(background, const.DMODE)
        self.background = pygame.Surface(const.DMODE)
        
        # track power bar, rocket, moon
        self.moon = moon.Moon()
        self.rocket = rocket.Rocket()
        self.pbar = powerbar.Powerbar()
        self.gbar = gravitybar.Gravitybar()

    def main(self):
        lev1 = level.Level(self, 0)
        lev1.main()

if __name__ == '__main__':
    gm = Game()
    gm.main()
