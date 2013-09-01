import pygame
import const
import data
import sys
import pygame
import powerbar, rocket, moon
#from pygame.locals import * # remove this later

class Game(object):
    def __init__(self):

        pygame.init()

        # set up screen etc.
        self.screen = pygame.display.set_mode(const.DMODE)
        self.clock = pygame.time.Clock()

        # background
        background = pygame.image.load(data.filepath('ghettoville2.jpg'\
                                                     )).convert_alpha()
        self.background = pygame.transform.scale(background, const.DMODE)

        # track power bar, rocket, moon
        self.moon = moon.Moon()
        self.hitmoon = False
        self.rocket = rocket.Rocket()
        self.pbar = powerbar.Powerbar()

        # sprite group stuff
        self.allsprites = pygame.sprite.RenderUpdates()
        self.allsprites.add(self.rocket)
        self.allsprites.add(self.moon)
        self.allsprites.add(self.pbar)

        # draw to screen
        self.allsprites.draw(self.screen)
        self.screen.blit(self.background, (0,0))
        pygame.display.flip()

    def off_screen(self, sprite):
        """Return true if sprite is offscreen (lazy version)"""
        swidth = self.screen.get_width()
        sheight = self.screen.get_height()
        if ((sprite.rect.left > swidth) or
            (sprite.rect.top > sheight) or
            (sprite.rect.right < 0) or (sprite.rect.bottom < 0)):
            return True
        return False

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

            # check if the rocket hit the moon!
            if pygame.sprite.collide_rect(self.rocket, self.moon):
                self.hitmoon = True
                #self.allsprites.remove(self.rocket)

            # render our sprites
            self.allsprites.clear(self.screen, self.background)
            dirty = self.allsprites.draw(self.screen)
            pygame.display.update(dirty)

if __name__ == '__main__':
    gm = Game()
    gm.main()
