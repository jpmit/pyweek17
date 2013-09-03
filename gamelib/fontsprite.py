import state
import pygame
import const

class LevelText(state.BaseSprite):
    # the loc is the top left of the rect
    LOC = (50, 20)

    def __init__(self, font, lnum = 1):

        super(LevelText, self).__init__()
        
        text = 'LEVEL: {0}'.format(lnum)
        self.image = font.render(text, True, const.WHITE)
        self.rect = self.image.get_rect()

        self.rect.topleft = LevelText.LOC

class DestroyedText(state.BaseSprite):
    # the loc is the top left of the rect
    LOC = (50, 60)

    def __init__(self, font, num=0):
        self.font = font
        super(DestroyedText, self).__init__()

        # this will sort out image and rect attributes
        self.set_destroyed(num)

    def set_destroyed(self, num):
        self.nnum = num
        text = 'ROCKETS DESTROYED: {0}'.format(num)
        self.image = self.font.render(text, True, const.WHITE)
        self.rect = self.image.get_rect()
        self.rect.topleft = DestroyedText.LOC
