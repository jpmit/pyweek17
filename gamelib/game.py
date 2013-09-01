import pygame
import const
import data
import sys
import sprites
import pygame
#from pygame.locals import * # remove this later

class Game(object):
    def __init__(self):

        pygame.init()

        # set up screen etc.
        self.screen = pygame.display.set_mode(const.DMODE)
        self.clock = pygame.time.Clock()

        # background
        background = pygame.image.load(data.filepath('ghettoville1.jpg'\
                                                     )).convert_alpha()
        self.background = pygame.transform.scale(background, const.DMODE)

        # sprite group stuff
        self.allsprites = pygame.sprite.OrderedUpdates()
        self.allsprites.add(sprites.Rocket((100,500)))
        self.allsprites.add(sprites.Moon((800,50)))

        self.allsprites.add(sprites.Powerbar())

        # draw to screen
        self.allsprites.draw(self.screen)
        self.screen.blit(self.background, (0,0))
        pygame.display.flip()

    def main(self):
    
        # main loop
        while True:
            dt = self.clock.tick(const.FPS)
            
            # handle events
            self.pressed = pygame.key.get_pressed()
            
            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    pygame.quit()
                    sys.exit()

            # update sprites
            self.allsprites.update(dt/1000.0, self)

            # render our sprites
            self.allsprites.clear(self.screen, self.background)
        
            dirty = self.allsprites.draw(self.screen)

            pygame.display.update(dirty)

        
