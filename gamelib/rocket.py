import state
import data
import pygame

class Rocket(state.BaseSprite):
    def __init__(self, xy):
        super(Rocket, self).__init__()
        # we need to rotate this baseimage
        self.baseimage = pygame.image.load(data.filepath('rocket.png')).\
                         convert_alpha()
        
        # initial image is the upright image
        self.image = self.baseimage
        self.rect = self.image.get_rect()
        self.rect.centerx, self.rect.centery = xy

        # orientation angle to vertical (clockwise in degrees)
        self.oangle = 0.0

        # add states to the statemachine
        onlaunchpad_state = RocketOnLaunchpadState(self)
        #launched_state = RocketLaunchedState(self)
        self.brain.add_state(onlaunchpad_state)
        #self.brain.add(launched_state)

        # start on the launchpad
        self.brain.set_state('onlaunchpad')

    def update(self, dt, game):
        # store the state of the game in the rocket object
        self.game = game
        self.dt = dt
        
        # do the thinking (and drawing)
        self.brain.think()

class RocketOnLaunchpadState(state.State):
    def __init__(self, rocket):
        
        super(RocketOnLaunchpadState, self).__init__('onlaunchpad')

        # store ref to object that we are a state of for manipulation
        self.rkt = rocket

    def do_actions(self):
        
        # time passed since last tick
        dt = self.rkt.dt
        
        # save old coordinates and old orientation angle
        ox, oy = self.rkt.rect.centerx, self.rkt.rect.centery
        oa = self.rkt.oangle

        if self.rkt.game.pressed[pygame.K_RIGHT]:
            # if we are pressing button, update orientation angle
            self.rkt.oangle -= dt*10.0
        if self.rkt.game.pressed[pygame.K_LEFT]:
            self.rkt.oangle += dt*10.0

        if self.rkt.oangle != oa:
            # we want to rotate the image
            self.rkt.image = pygame.transform.rotate(self.rkt.baseimage,
                                                     self.rkt.oangle)
            self.rkt.rect = self.rkt.image.get_rect()
            self.rkt.rect.centerx = ox
            self.rkt.rect.centery = oy

    def check_conditions(self):
        pass

    def entry_actions(self):
        pass

    def exit_actions(self):
        pass
