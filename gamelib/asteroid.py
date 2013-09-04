import pygame
import state
import data
import const

class Asteroid(state.BaseSprite):
    NFRAMES = 15 # number of frames before changing image!
    def __init__(self, game, pos):

        super(Asteroid, self).__init__()

        # the four images used for the asteroid rotation animation
        self.imarray = [game.astim1, game.astim2,
                        game.astim3, game.astim4]
        self.numimg = 4

        self.pos = pos
        self.nfr = 0
        self.inum = 0 # index into images array
        self.set_image()

    def set_image(self):

        self.image = self.imarray[self.inum]
        self.rect = self.image.get_rect()

        # change frame
        self.inum = (self.inum + 1) % self.numimg

        # change position of rect
        self.rect.centerx, self.rect.centery = self.pos

    def update(self, dt, game):
        self.nfr += 1
        if self.nfr == self.NFRAMES:
            self.set_image()
            self.nfr = 0
