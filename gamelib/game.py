import pygame
import const
import data
import sys
import pygame
import powerbar, rocket, moon, gravitybar, fontsprite
import level
import scrolling

class Game(object):
    # collision constants
    CRECTROID = 0.5 # for asteroid
    CRECTMOON = 0.7 # for moon
    def __init__(self):

        pygame.init()

        # set up screen etc.
        self.screen = pygame.display.set_mode(const.DMODE)
        self.swidth = self.screen.get_width()
        self.sheight = self.screen.get_height()        

        # for getting right FPS
        self.clock = pygame.time.Clock()

        # background
        background = pygame.image.load(data.filepath('stars.png'\
                                                     )).convert_alpha()
        #background = pygame.Surface(const.DMODE)
        #background.fill(const.BCOLOR)
        self.background = background
        #self.background = pygame.transform.scale(background, const.DMODE)
        # black background for now
        #self.background = pygame.Surface(const.DMODE)
        
        self.load_sounds()
        if self.soundon:
            pygame.mixer.music.set_volume(0.8)
            pygame.mixer.music.play(-1)

        self.load_fonts()

        self.store_globals()

    def load_sounds(self):
        try:
            pygame.mixer.init()
        except:
            print 'Cannot load sound'
            self.soundon = False
        finally:
            pygame.mixer.music.load(data.filepath('purity.ogg'))
            self.sfx = {'click': pygame.mixer.Sound(data.filepath('click.ogg')),
                        'complete': pygame.mixer.Sound(data.filepath('complete.ogg')),
                        'hitroid': pygame.mixer.Sound(data.filepath('atari.ogg')),
                        'error': pygame.mixer.Sound(data.filepath('error.ogg')),
                        'pbar': pygame.mixer.Sound(data.filepath('pbar2.ogg'))
                        }
            self.soundon = True

    def load_fonts(self):
        self.levelfont = pygame.font.Font(data.filepath('chalkdust.ttf'),20)
        self.destfont = pygame.font.Font(data.filepath('chalkdust.ttf'),20)        

    def store_globals(self):
        """We store references to some things here that are needed all
        over the game."""

        # the main sprites
        self.moon = moon.Moon(self)
        self.rocket = rocket.Rocket(self)
        self.pbar = powerbar.Powerbar(self)
        self.gbar = gravitybar.Gravitybar(self)

        # some states needed by many objects
        self.hitmoon = False
        self.rktdead = False # dead if gone off-screen
        self.hitasteroid = False

        # number of rockets destroyed so far in game
        self.numdestroyed = 0
        self.destroyedtext = fontsprite.DestroyedText(self.destfont)

        # collision functions
        # rocket with asteroids
        self.collide_roid = pygame.sprite.collide_rect_ratio(Game.\
                                                               CRECTROID)
        # rocke              t with moon
        self.collide_moon = pygame.sprite.collide_rect_ratio(Game.\
                                                             CRECTMOON)
        
        # scroller handles moving screen and sprites etc
        self.scroller = scrolling.Scroller(self)


    def main(self):
        for levnum in [1,2]:#[0,1,2,3,4]:
            nextlevel = level.Level(self, levnum)
            nextlevel.main()
        pygame.quit()

if __name__ == '__main__':
    gm = Game()
    gm.main()
