import pygame
import const
import data
import sys
import pygame
import powerbar, rocket, moon, gravitybar, fontsprite
import level
import scrolling
import menu
import leveldata

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
        pygame.display.set_caption('Moon Lander')

        # for getting right FPS
        self.clock = pygame.time.Clock()

        # background
        self.background = pygame.image.load(data.filepath('stars.png'\
                                                          )).convert_alpha()
        
        self.load_sounds()
        self.load_fonts()
        self.load_images()
        self.store_globals()

    def load_sounds(self):
        """Load ALL of the sounds used in the game."""
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
                        'pbar': pygame.mixer.Sound(data.filepath('pbar.ogg')),
                        'startgame': pygame.mixer.Sound(data.filepath('startgame.ogg'))
                        }
            self.soundon = True

    def load_fonts(self):
        """Load ALL of the fonts usedin the game."""
        self.levelfont = pygame.font.Font(data.filepath('chalkdust.ttf'), 20)
        self.destfont = pygame.font.Font(data.filepath('chalkdust.ttf'), 20)
        self.barfont = pygame.font.Font(data.filepath('chalkdust.ttf'), 16)
        self.menufont = pygame.font.Font(data.filepath('chalkdust.ttf'), 64)
        self.helpfont = pygame.font.Font(data.filepath('chalkdust.ttf'), 32)

    def load_images(self):
        """Load the asteroid animation images only.  Others are loaded
        elsewhere."""
        self.astim1 = pygame.image.load(data.filepath('roid1.png')).\
              convert_alpha()
        self.astim2 = pygame.image.load(data.filepath('roid2.png')).\
              convert_alpha()        
        self.astim3 = pygame.image.load(data.filepath('roid3.png')).\
              convert_alpha()        
        self.astim4 = pygame.image.load(data.filepath('roid4.png')).\
              convert_alpha()

    def reset_globals(self):
        self.store_globals()

    def store_globals(self):
        """We store references to some things here that are needed all
        over the game."""

        # number of levels
        self.numlevels = len(leveldata.ALLDATA)

        # the main sprites
        self.moon = moon.Moon(self)
        self.rocket = rocket.Rocket(self)
        self.pbar = powerbar.Powerbar(self)
        self.gbar = gravitybar.Gravitybar(self)

        # text 'gravity' and 'power' for status bars are stored as
        # additional sprites
        self.pbartext = fontsprite.FontSprite(self.barfont, 'power',
                                              fontsprite.PBARLOC)
        self.gbartext = fontsprite.FontSprite(self.barfont, 'gravity',
                                              fontsprite.GBARLOC)

        # some states needed by many objects
        self.hitmoon = False
        self.rktdead = False # dead if gone off-screen
        self.hitasteroid = False

        # number of rockets destroyed so far in game
        self.numdestroyed = 0
        self.destroyedtext = fontsprite.FontSprite(self.destfont,
                                                   '{0}{1}'.format\
                                                   (fontsprite.DTEXT,0),
                                                   fontsprite.DESTLOC)

        # collision functions
        # rocket with asteroids (scaled rect collision)
        self.collide_roid = pygame.sprite.collide_rect_ratio(Game.\
                                                               CRECTROID)
        # rocket with moon ('pixel perfect' collision)
        self.collide_moon = pygame.sprite.collide_mask

        # scroller handles moving screen and sprites etc
        self.scroller = scrolling.Scroller(self)

    def main(self, startlevel):

        # refresh globals - this is really for second time round,
        # i.e. so we reset num rockets destroyed to zero
        self.reset_globals()

        # this is to make the sound effects louder relative to the
        # background music, but I'm not sure it works like that...
        pygame.mixer.music.set_volume(0.8)

        # loop the main music
        pygame.mixer.music.play(-1)
        
        # main game        
        for levnum in range(startlevel, self.numlevels):
            nextlevel = level.Level(self, levnum)
            nextlevel.main()
