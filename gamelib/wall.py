import pygame
import state
import const
import data

THICKNESS = 10 # width of wall in pixels
COLOR = (31, 31, 144) # wall color

class SideWall(state.BaseSprite):
    def __init__(self, height, pos):
        super(SideWall, self).__init__()
        
        self.image = pygame.Surface((THICKNESS, height))
        self.image.fill(COLOR)
        self.rect = self.image.get_rect()
        self.rect.topleft = pos
        pass
        
class TopWall(state.BaseSprite):
    def __init__(self, width, pos):
        super(TopWall, self).__init__()
        
        self.image = pygame.Surface((width, THICKNESS))
        self.image.fill(COLOR)
        self.rect = self.image.get_rect()
        self.rect.topleft = pos        
        pass

class Arrow(state.BaseSprite):
    # the directions
    LEFT = 'left'
    RIGHT = 'right'
    UP = 'up'
    DOWN = 'down'
    DISP = 30
    LOCS = {LEFT: (DISP, const.DMODE[1]/2),
            RIGHT: (const.DMODE[0] - DISP, const.DMODE[1]/2) ,
            UP: (const.DMODE[0]/2 , DISP) ,
            DOWN: (const.DMODE[0]/2, const.DMODE[1] - DISP) }
    BLINKTIME = 0.5 # in seconds
    def __init__(self, direction):
        super(Arrow, self).__init__()

        # this is the left one
        self.baseimage = pygame.image.load(data.filepath('arrow.png')).convert_alpha()
        if direction == Arrow.DOWN:
            rot = 90
        elif direction == Arrow.RIGHT:
            rot = 180
        elif direction == Arrow.UP:
            rot = 270
            
        # rotate the image
        if direction != Arrow.LEFT:
            self.baseimage = pygame.transform.rotate(self.baseimage, rot)
        self.image = self.baseimage
        self.rect = self.image.get_rect()
        
        # set position
        self.rect.center = Arrow.LOCS[direction]
        
        # blank image for flashing animation
        self.blankimage = pygame.Surface([self.rect.width, self.rect.height],
                                         pygame.SRCALPHA, 32).convert_alpha()
        
        # allow switching between base and blank images
        self.images = [self.baseimage, self.blankimage]
        self.numimages = len(self.images)
        self.inum = 0

        # track time passed since image altered
        self.tpassed = 0.0

    def reset(self):
        self.tpassed = 0.0
        self.inum = 0
        self.image = self.images[self.inum]

    def update(self, dt, game):
        self.tpassed += dt
        if self.tpassed > Arrow.BLINKTIME:
            self.tpassed = 0.0
            # set new image
            self.inum += 1
            self.inum = self.inum % self.numimages
            self.image = self.images[self.inum]
