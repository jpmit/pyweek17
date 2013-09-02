import pygame
import state
import const

THICKNESS = 5 # width of wall in pixels
COLOR = const.RED

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
