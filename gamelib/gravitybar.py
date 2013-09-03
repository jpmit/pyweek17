import pygame
import state
import const

class Gravitybar(state.BaseSprite):
    WIDTH = 80
    HEIGHT = 100
    GLEVELS = [0.2,0.4,0.8,1.3,2.0]
    MAXBARS = len(GLEVELS) - 1
    BORDER = 6
    LOCATION = (460, 530)
    BARCOLOR = (241, 108, 28)
    def __init__(self, game):
        super(Gravitybar, self).__init__()

        self.game = game

        # full and empty bars (pygame surfaces)
        self.barheight = int(float(Gravitybar.HEIGHT)/Gravitybar.MAXBARS)
        self.fbar = pygame.Surface((Gravitybar.WIDTH - 2*Gravitybar.BORDER,
                                    self.barheight - 2*Gravitybar.BORDER))

        self.fbar.fill(Gravitybar.BARCOLOR)
        self.ebar = self.fbar.copy()
        self.ebar.fill(const.WHITE)

        self.empty_bar()
        self.nbars = 0 # number of full bars

        # add states to the statemachine
        active_state = GravitybarActiveState(self)
        notactive_state = GravitybarNotActiveState(self)
        self.brain.add_state(active_state)
        self.brain.add_state(notactive_state)

    def set_start_state(self):
        # start in the active state
        self.brain.set_state('active')

    def get_gravity(self):
        return Gravitybar.GLEVELS[self.nbars]

    def add_bar(self):
        """Add one bar to the gravity meter and change gravity
        accordingly."""
        if self.nbars < Gravitybar.MAXBARS:
            # get x pos and y pos to blit bar to
            ybl = Gravitybar.HEIGHT - (self.nbars + 1)*self.barheight + Gravitybar.BORDER
            xbl = Gravitybar.BORDER
            self.image.blit(self.fbar, (xbl, ybl))
            self.nbars += 1
            # play sound!
            self.game.sfx['click'].play()
        else:
            # play not possible sound effect
            self.game.sfx['error'].play()

    def remove_bar(self):
        """Remove one bar from the gravity meter and change gravity
        accordingly."""
        if self.nbars > 0:
            # get x pos and y pos to blit bar to
            ybl = Gravitybar.HEIGHT - (self.nbars)*self.barheight + Gravitybar.BORDER
            xbl = Gravitybar.BORDER
            self.image.blit(self.ebar, (xbl, ybl))
            self.nbars -= 1
            # play sound!
            self.game.sfx['click'].play()
        else:
            # play not possible sound effect
            self.game.sfx['error'].play()

    def empty_bar(self):
        """Draw an empty gravity bar at the correct place on the screen"""
        
        # surface starts as a white rectangle
        self.image = pygame.Surface((Gravitybar.WIDTH, Gravitybar.HEIGHT))
        self.image.fill(const.WHITE)

        # draw the black border onto the white rectangle
        self.rect = self.image.get_rect()
        pygame.draw.rect(self.image, const.BLACK,
                         self.rect,
                         Gravitybar.BORDER)

        # draw the black outlines for each bar
        for i in range(Gravitybar.MAXBARS):
            pygame.draw.rect(self.image, const.BLACK,
                             (self.rect.left, self.rect.top + self.barheight*i,
                              Gravitybar.WIDTH, self.barheight),
                             Gravitybar.BORDER)

        # position the image
        self.rect.centerx, self.rect.centery = Gravitybar.LOCATION

    def update(self, dt, game):
        # store the state of the game in the gravitybar object
        self.game = game
        self.dt = dt
        
        # do the thinking
        self.brain.think()

class GravitybarNotActiveState(state.State):
    """In the notactive state, the gravity bar will not respond to key
    up and key down events."""
    def __init__(self, gravitybar):
        
        super(GravitybarNotActiveState, self).__init__('notactive')

        # store ref to object so we can alter it
        self.gbar = gravitybar

    def check_conditions(self):
        if (self.gbar.game.rocket.brain.get_state() == 'onlaunchpad'
            and self.gbar.game.pbar.brain.get_state() == 'idle') :
            return 'active'

class GravitybarActiveState(state.State):
    """In the active state, the gravity bar will respond to key up and
    key down events."""
    def __init__(self, gravitybar):
        
        super(GravitybarActiveState, self).__init__('active')

        # store ref to object that we are a state of for manipulation
        self.gbar = gravitybar

    def entry_actions(self):
        """Make the gravity bar roughly half full!"""
        for i in range(Gravitybar.MAXBARS / 2):
            #self.gbar.add_bar()
            pass

    def do_actions(self):

        # time passed since last ticke
        dt = self.gbar.dt
        
        if pygame.K_UP in self.gbar.game.keyup:
            self.gbar.add_bar()

        if pygame.K_DOWN in self.gbar.game.keyup:
            self.gbar.remove_bar()

    def check_conditions(self):
        # if we have pressed the spacebar, then we have entered the
        # launch sequence and we dont want to respond to key up and down events
        if self.gbar.game.pressed[pygame.K_SPACE]:
            return 'notactive'
