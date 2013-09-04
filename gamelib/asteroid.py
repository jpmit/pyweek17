import pygame
import state
import data
import const

class Asteroid(state.BaseSprite):
    NFRAMES = 15 # number of frames before changing image!
    def __init__(self, pos):

        super(Asteroid, self).__init__()

        # move this later, we don't want to load images every time!
        self.load_images()

        self.pos = pos
        self.nfr = 0
        self.inum = 0 # index into images array
        self.set_image()

    def load_images(self):
        # 1st, 3rd, 6th and 13th image from the big spritesheet
        im1 = pygame.image.load(data.filepath('roid1.png')).\
              convert_alpha()
        im2 = pygame.image.load(data.filepath('roid2.png')).\
              convert_alpha()        
        im3 = pygame.image.load(data.filepath('roid3.png')).\
              convert_alpha()        
        im4 = pygame.image.load(data.filepath('roid4.png')).\
              convert_alpha()

        self.imarray = [im1, im2, im3, im4]
        self.numimg = len(self.imarray)

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
