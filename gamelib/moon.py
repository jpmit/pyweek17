import pygame
import state
import const

class Moon(state.BaseSprite):
    def __init__(self, xy):
        
        super(Moon, self).__init__()
        self.image = pygame.Surface((80,80))
        srect = self.image.get_rect()
        self.rect = pygame.draw.circle(self.image, const.WHITE,
                                        (srect.centerx,
                                        srect.centery), 40)
        self.rect.centerx, self.rect.centery = xy        

    def update(self, dt, game):
        #self.rect.right += dt*200
        pass
