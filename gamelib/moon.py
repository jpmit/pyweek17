import pygame
import state
import const
import data

class Moon(state.BaseSprite):
    # this is a square sprite at the moment
    DIAMETER = 80
    def __init__(self, game):

        self.game = game

        super(Moon, self).__init__()
        #self.image = pygame.Surface((Moon.DIAMETER, Moon.DIAMETER), pygame.SRCALPHA,
        #                            32).convert_alpha()
        self.baseimage = pygame.image.load(data.filepath('moon.png')).convert_alpha()
        self.hitimage =  pygame.image.load(data.filepath('moonhit2.png')).convert_alpha()
        self.image = self.baseimage
        self.rect = self.image.get_rect()

        # for colliding using circles, if we end up using this
        self.radius = Moon.DIAMETER/2

        # for mask collide, again if we use it
        self.mask = pygame.mask.from_surface(self.image)

        # we update the position at the start of every level
        self.pos = (0, 0)

        # add states
        idle_state = MoonIdleState(self)
        hit_state = MoonHitState(self)
        self.brain.add_state(idle_state)
        self.brain.add_state(hit_state)

    def set_start_state(self):
        """Set state to be start of level state"""
        self.brain.set_state('idle')

    def set_pos(self, pos):
        self.pos = pos
        self.rect.center = self.pos
        
    def update(self, dt, game):
        self.game = game
        self.dt = dt

        # do the thinking (and drawing)
        self.brain.think()

class MoonIdleState(state.State):
    def __init__(self, moon):

        super(MoonIdleState, self).__init__('idle')
        self.moon = moon

    def check_conditions(self):
        if self.moon.game.hitmoon:
            return 'hit'

    def entry_actions(self):
        """Draw the moon in the correct position"""
        #pygame.draw.circle(self.moon.image, const.WHITE,
        #                   (Moon.DIAMETER/2, Moon.DIAMETER/2),
        #                   Moon.DIAMETER/2)
        self.moon.rect.center = self.moon.pos

class MoonHitState(state.State):
    def __init__(self, moon):

        super(MoonHitState, self).__init__('hit')
        self.moon = moon

    def entry_actions(self):
        # play sound effect
        self.moon.game.sfx['complete'].play()
        self.moon.image = self.moon.hitimage
        
    def check_conditions(self):
        # We'll be rescued next level!
        pass

    def exit_actions(self):
        self.moon.image = self.moon.baseimage
