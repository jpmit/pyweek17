import pygame
import state
import const

class Powerbar(state.BaseSprite):
    WIDTH = 300
    HEIGHT = 80
    BORDER = 5
    MAXFULL = 1.0
    LOCATION = (180, 700)
    def __init__(self):
        super(Powerbar, self).__init__()

        self.empty_bar()

        # fullness is between 0.0 and 1.0 (the amount of 'red' in bar)
        self.fullness = 0.0

        # add states to the statemachine
        idle_state = PowerbarIdleState(self)
        inlaunch_state = PowerbarInlaunchState(self)
        fired_state = PowerbarFiredState(self)
        self.brain.add_state(idle_state)
        self.brain.add_state(inlaunch_state)
        self.brain.add_state(fired_state)        

        # start in the idle (empty) state
        self.brain.set_state('idle')

    def empty_bar(self):
        """Draw an empty power bar at the correct place on the screen"""
        
        # surface starts as a white rectangle
        self.image = pygame.Surface((Powerbar.WIDTH, Powerbar.HEIGHT))
        self.image.fill(const.WHITE)

        # draw the black border onto the white rectangle
        self.rect = self.image.get_rect()
        pygame.draw.rect(self.image, const.BLACK,
                         self.image.get_rect(),
                         Powerbar.BORDER)

        # position the image
        self.rect.centerx, self.rect.centery = Powerbar.LOCATION

    def update(self, dt, game):
        # store the state of the game in the powerbar object
        self.game = game
        self.dt = dt
        
        # do the thinking
        self.brain.think()

class PowerbarIdleState(state.State):
    def __init__(self, powerbar):
        
        super(PowerbarIdleState, self).__init__('idle')

        # store ref to object that we are a state of for manipulation
        self.pbar = powerbar

    def check_conditions(self):
        if self.pbar.game.pressed[pygame.K_SPACE]:
            return 'inlaunch'

class PowerbarInlaunchState(state.State):
    def __init__(self, powerbar):
        
        super(PowerbarInlaunchState, self).__init__('inlaunch')

        # store ref to object that we are a state of for manipulation
        self.pbar = powerbar

    def do_actions(self):

        # time passed since last ticke
        dt = self.pbar.dt
        
        if self.pbar.game.pressed[pygame.K_SPACE]:
            
            if self.pbar.fullness < Powerbar.MAXFULL:
                # get new fullness of power bar
                self.pbar.fullness += dt * 1.0
                # set it to fullness if we have gone beyond it
                if self.pbar.fullness > Powerbar.MAXFULL:
                    self.pbar.fullness = Powerbar.MAXFULL
                    
                # surface for the red part of the status bar
                rsurf = pygame.Surface(((Powerbar.WIDTH - Powerbar.BORDER*2)\
                                        *self.pbar.fullness,
                                        (Powerbar.HEIGHT - Powerbar.BORDER*2)))
                rsurf.fill(const.RED)
                # blit the red surface onto the main surface
                self.pbar.image.blit(rsurf, (Powerbar.BORDER, Powerbar.BORDER))

    def check_conditions(self):
        # if we have released the spacebar, then we have fired the rocket
        if not self.pbar.game.pressed[pygame.K_SPACE]:
            return 'fired'

class PowerbarFiredState(state.State):
    def __init__(self, powerbar):
        
        super(PowerbarFiredState, self).__init__('fired')

        # store ref to object that we are a state of for manipulation
        self.pbar = powerbar

    def entry_actions(self):
        # draw an empty power bar
        self.pbar.empty_bar()

    def check_conditions(self):
        # go back to idle state for now so we can repeatedly fire
        return 'idle'

    def exit_actions(self):
        self.pbar.fullness = 0.0

