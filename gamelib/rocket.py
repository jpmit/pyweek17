import state
import data
import pygame
import math
import time
import fontsprite
import spritesheet
import const

class Rocket(state.BaseSprite):
    # x and y speed per frame (these should probably be equal)
    XSPEED = 300
    YSPEED = 300
    WINDACC = (0.0, 0.0)
    # how quickly angle changes on launchpad
    ROTSPEED = 100
    # launchpad location
    LAUNCHLOC = (100, 480)
    
    def __init__(self, game):
        super(Rocket, self).__init__()

        self.game = game
        
        # we need to rotate this baseimage
        baseimage = pygame.image.load(data.filepath('smallrocket.png')).\
                    convert_alpha()
        # height and width of base image
        height, width = baseimage.get_width(), baseimage.get_height()
        self.baseimage = baseimage
        
        # initial image is the upright image
        self.image = self.baseimage
        self.rect = self.image.get_rect()

        # mask used for checking collision with moon
        self.mask = pygame.mask.from_surface(self.image)

        # orientation angle to vertical (clockwise in degrees)
        self.oangle = 0.0

        # blank image for when we hit moon
        self.blankimage = pygame.Surface((self.rect.width, self.rect.height),
                                         pygame.SRCALPHA, 32).convert_alpha()

        # images for explosion animation - only use last 9!
        self.explodeimages = spritesheet.Spritesheet('explode.png').\
                             all_images(4, 4, 100, 100)[:9]
        self.numexplode = len(self.explodeimages)

        # add states to the statemachine
        onlaunchpad_state = RocketOnLaunchpadState(self)
        fired_state = RocketFiredState(self)
        hitmoon_state = RocketHitMoonState(self)
        hitasteroid_state = RocketHitAsteroidState(self)        
        self.brain.add_state(onlaunchpad_state)
        self.brain.add_state(fired_state)
        self.brain.add_state(hitmoon_state)
        self.brain.add_state(hitasteroid_state)

    def set_start_state(self):
        """Set state to be start of level state"""
        self.fangle = 0.0
        self.brain.set_state('onlaunchpad')

    def draw(self, xy):
        """Draw rocket at coords xy clockwise by angle to vertical"""
        # pygame rotates counter-clockwise by default so negate argument
        self.image = pygame.transform.rotate(self.baseimage,
                                             -self.oangle)
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
        self.rkt.xvel = math.sin(oanglerad)*math.exp(self.rkt.game.pbar.fullness)
        self.rkt.yvel = math.cos(oanglerad)*math.exp(self.rkt.game.pbar.fullness)

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
        angle = (180.0/math.pi) * math.acos(self.rkt.yvel /
                                            (self.rkt.xvel**2 + self.rkt.yvel**2)**0.5)
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

        if self.rkt.game.hitasteroid:
            return 'hitasteroid'

        if self.rkt.game.hitmoon:
            return 'hitmoon'
        pass

class RocketHitAsteroidState(state.State):
    def __init__(self, rocket):
        
        super(RocketHitAsteroidState, self).__init__('hitasteroid')

        # store ref to object that we are a state of for manipulation
        self.rkt = rocket

        # for controlling explosion
        self.explosiondone = False
        self.ncalled = 0
        self.numframes = 9 # frames for each explosion image
        self.exindx = -1

    def set_explosion_image(self):
        if not self.ncalled % self.numframes:
            self.exindx -= 1
            self.rkt.image = self.rkt.explodeimages[self.exindx]
        self.ncalled += 1

    def do_actions(self):
        # do some explosion
        self.set_explosion_image()

        if (self.exindx == -self.rkt.numexplode + 1):
            self.explosiondone = True

    def entry_actions(self):
        self.rkt.game.numdestroyed += 1
        self.rkt.game.destroyedtext.set_text('{0}{1}'.\
                                             format(fontsprite.DTEXT,
                                                    self.rkt.game.numdestroyed))
        self.rkt.game.sfx['hitroid'].play()

    def check_conditions(self):
        if self.explosiondone:
            return 'onlaunchpad'

    def exit_actions(self):
        self.explosiondone = False
        self.ncalled = 0
        self.exindx = -1

class RocketHitMoonState(state.State):
    FRAMES = 100
    def __init__(self, rocket):
        
        super(RocketHitMoonState, self).__init__('hitmoon')

        # store ref to object that we are a state of for manipulation
        self.rkt = rocket

    def entry_actions(self):
        self.nframes = 0
        # set blank image
        self.rkt.image = self.rkt.blankimage
        pass

    def do_actions(self):
        self.nframes += 1
        

    def check_conditions(self):
        if self.nframes == RocketHitMoonState.FRAMES:
            return 'onlaunchpad'

class RocketOnLaunchpadState(state.State):
    def __init__(self, rocket):
        
        super(RocketOnLaunchpadState, self).__init__('onlaunchpad')

        # store ref to object that we are a state of for manipulation
        self.rkt = rocket

    def entry_actions(self):
        """Move the rocket onto the launchpad"""
        self.rkt.oangle =  self.rkt.fangle
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

        # move rocket manually for collision debugging aka GODMODE
        if const.GODMODE:
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

    def exit_actions(self):
        """Save the orientation angle we were fired at so we can put
        back on launchpad at this angle."""
        self.rkt.fangle = self.rkt.oangle
