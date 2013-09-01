import state
import data
import pygame
import math

class Rocket(state.BaseSprite):
    # size of rocket
    SIZE = (20,90)
    # x and y speed per frame
    XSPEED = 1000
    YSPEED = 1000
    WINDACC = (0.0, 0.0)
    # how quickly angle changes on launchpad
    ROTSPEED = 100
    # launchpad location
    LAUNCHLOC = (100, 600)
    
    def __init__(self):
        super(Rocket, self).__init__()
        
        # we need to rotate this baseimage
        baseimage = pygame.image.load(data.filepath('rocket.png')).\
                    convert_alpha()
        # height and width of base image
        height, width = baseimage.get_width(), baseimage.get_height()
        # make it smaller!!
        self.baseimage = pygame.transform.scale(baseimage, Rocket.SIZE)
        
        # initial image is the upright image
        self.image = self.baseimage
        self.rect = self.image.get_rect()

        # orientation angle to vertical (clockwise in degrees)
        self.oangle = 0.0

        # add states to the statemachine
        onlaunchpad_state = RocketOnLaunchpadState(self)
        fired_state = RocketFiredState(self)
        hitmoon_state = RocketHitMoonState(self)
        self.brain.add_state(onlaunchpad_state)
        self.brain.add_state(fired_state)
        self.brain.add_state(hitmoon_state)        

        # start on the launchpad
        self.brain.set_state('onlaunchpad')

    def draw(self, xy):
        """Draw rocket at coords xy clockwise by angle to vertical"""
        # pygame rotates counter-clockwise by default so negate argument
        self.image = pygame.transform.rotate(self.baseimage, -self.oangle)
        self.rect = self.image.get_rect()
        self.rect.centerx, self.rect.centery = xy

    def update(self, dt, game):
        # store the state of the game in the rocket object
        self.game = game
        self.dt = dt

        # do the thinking (and drawing)
        self.brain.think()

class RocketFiredState(state.State):
    def __init__(self, rocket):

        super(RocketFiredState, self).__init__('fired')

        # store ref to object that we are a state of for manipulation
        self.rkt = rocket

    def entry_actions(self):
        # convert orientation angle to radians!
        oanglerad = self.rkt.oangle*math.pi / 180.0
        
        # set initial x velocity and y velocity of rocket according to
        # the angle I am aiming at, and the fullness of the powerbar
        self.rkt.xvel = math.sin(oanglerad)*self.rkt.game.pbar.fullness
        self.rkt.yvel = math.cos(oanglerad)*self.rkt.game.pbar.fullness

        # get gravity level from gravity bar
        Rocket.GRAVITY = self.rkt.game.gbar.get_gravity()

    def do_actions(self):
        # move the rocket
        dt = self.rkt.dt

        # change the velocity according to gravity
        dvy = -Rocket.GRAVITY*dt
        self.rkt.yvel += dvy

        self.rkt.rect.centerx += self.rkt.xvel*dt*Rocket.XSPEED
        self.rkt.rect.centery -= self.rkt.yvel*dt*Rocket.YSPEED

        # work out angle that rocket is pointing (clockwise from
        # horizontal) based on speed and draw the rocket at that angle
        angle = (180.0/math.pi) * math.acos( self.rkt.yvel / (self.rkt.xvel**2 + self.rkt.yvel**2)**0.5)
        if self.rkt.xvel < 0.0:
            angle = -angle
        self.rkt.oangle = angle

        # draw the rocket
        self.rkt.draw((self.rkt.rect.centerx, self.rkt.rect.centery))

    def check_conditions(self):
        # check if we went off the screen, back to idle state!
        if self.rkt.game.rktdead:
            self.rkt.game.rktdead = False
            return 'onlaunchpad'

        if self.rkt.game.hitmoon:
            return 'hitmoon'
        pass

class RocketHitMoonState(state.State):
    def __init__(self, rocket):
        
        super(RocketHitMoonState, self).__init__('hitmoon')

        # store ref to object that we are a state of for manipulation
        self.rkt = rocket

    def entry_actions(self):
        # put an explosion animation somewhere
        pass

    def check_conditions(self):
        if self.rkt.game.pressed[pygame.K_RETURN]:
            # this is slightly dodgy organisation of code?
            self.rkt.game.hitmoon = False
            return 'onlaunchpad'

class RocketOnLaunchpadState(state.State):
    def __init__(self, rocket):
        
        super(RocketOnLaunchpadState, self).__init__('onlaunchpad')

        # store ref to object that we are a state of for manipulation
        self.rkt = rocket

    def entry_actions(self):
        """Move the rocket onto the launchpad"""
        self.rkt.oangle =  0.0
        self.rkt.draw(Rocket.LAUNCHLOC)
        
    def do_actions(self):

        # time passed since last tick
        dt = self.rkt.dt
        
        # save old coordinates and old orientation angle
        oa = self.rkt.oangle

        if self.rkt.game.pressed[pygame.K_RIGHT]:
            # if we are pressing button, update orientation angle
            self.rkt.oangle += dt*Rocket.ROTSPEED
        if self.rkt.game.pressed[pygame.K_LEFT]:
            self.rkt.oangle -= dt*Rocket.ROTSPEED

        # move rocket manually for collision debugging, remove this later
        if self.rkt.game.pressed[pygame.K_w]:
            self.rkt.rect.centery -= 10
        if self.rkt.game.pressed[pygame.K_s]:            
            self.rkt.rect.centery += 10
        if self.rkt.game.pressed[pygame.K_d]:            
            self.rkt.rect.centerx += 10
        if self.rkt.game.pressed[pygame.K_a]:            
            self.rkt.rect.centerx -= 10

        if self.rkt.oangle != oa:
            # we are oriented at a different angle to previously
            self.rkt.draw((self.rkt.rect.centerx, self.rkt.rect.centery))

    def check_conditions(self):

        # check if the powerbar is in the 'fired' state
        if self.rkt.game.pbar.brain.active_state.name == 'fired':
            return 'fired'
        pass
