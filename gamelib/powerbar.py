import pygame
import state
import const

class Powerbar(state.BaseSprite):
    WIDTH = 300
    HEIGHT = 50
    BORDER = 6
    MAXFULL = 1.0
    LOCATION = (180, 560)
    def __init__(self, game):
        super(Powerbar, self).__init__()

        self.game = game

        self.empty_bar()

        # fullness is between 0.0 and MAXFULL (the amount of 'red' in bar)
        self.fullness = 0.0

        # add states to the statemachine
        idle_state = PowerbarIdleState(self)
        inlaunch_state = PowerbarInlaunchState(self)
        fired_state = PowerbarFiredState(self)
        holding_state = PowerbarHoldingState(self)
        self.brain.add_state(idle_state)
        self.brain.add_state(inlaunch_state)
        self.brain.add_state(fired_state)
        self.brain.add_state(holding_state)        

        self.sound = self.game.sfx['pbar']

    def set_start_state(self):
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
        self.rect.center = Powerbar.LOCATION

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

        # time passed since last tick
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
                rsurf.fill(const.PBARCOLOR)
                # blit the red surface onto the main surface
                self.pbar.image.blit(rsurf, (Powerbar.BORDER, Powerbar.BORDER))

    def check_conditions(self):
        # if we have released the spacebar, then we have fired the rocket
        if not self.pbar.game.pressed[pygame.K_SPACE]:
            return 'fired'

    def entry_actions(self):
        # play the 'wooshing' effect
        self.pbar.sound.play()        

    def exit_actions(self):
        # stop the 'wooshing' effect        
        self.pbar.sound.stop()        
        pass

class PowerbarHoldingState(state.State):
    # has been fired but not yet ready to go back into idle state
    def __init__(self, powerbar):
        super(PowerbarHoldingState, self).__init__('holding')
        self.pbar = powerbar

    def check_conditions(self):
        if self.pbar.game.rocket.brain.get_state() == 'onlaunchpad':
            return 'idle'
        
    def exit_actions(self):
        # empty the bar!
        self.pbar.empty_bar()                
        self.pbar.fullness = 0.0

class PowerbarFiredState(state.State):
    INSTATE = 1 # number of frames we need to be in this state for
    def __init__(self, powerbar):
        
        super(PowerbarFiredState, self).__init__('fired')

        # store ref to object that we are a state of for manipulation
        self.pbar = powerbar

    def entry_actions(self):
        self.instate = 0
        pass

    def check_conditions(self):
        # we just need to be in this state long enough so that the rocket can
        # check our state
        if self.instate == PowerbarFiredState.INSTATE:
            return 'holding'

        self.instate += 1
