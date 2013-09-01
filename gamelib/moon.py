import pygame
import state
import const

class Moon(state.BaseSprite):
    # this is a square sprite at the moment
    DIAMETER = 80
    LOCATION = (800, 50)
    def __init__(self):

        super(Moon, self).__init__()
        self.image = pygame.Surface((Moon.DIAMETER, Moon.DIAMETER))
        self.rect = self.image.get_rect()

        # add states
        idle_state = MoonIdleState(self)
        hit_state = MoonHitState(self)
        self.brain.add_state(idle_state)
        self.brain.add_state(hit_state)

        # go into idle state
        self.brain.set_state('idle')
        
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
        pygame.draw.circle(self.moon.image, const.WHITE,
                           (Moon.DIAMETER/2, Moon.DIAMETER/2),
                           Moon.DIAMETER/2)
        self.moon.rect.center = Moon.LOCATION

class MoonHitState(state.State):
    def __init__(self, moon):

        super(MoonHitState, self).__init__('hit')
        self.moon = moon

    def entry_actions(self):
        # we've just been hit - draw the moon as being red
        srect = self.moon.image.get_rect()
        pygame.draw.circle(self.moon.image, const.RED,
                           (40,40), 40)
        self.moon.rect.centerx, self.moon.rect.centery = Moon.LOCATION
        
    def check_conditions(self):
        if self.moon.game.pressed[pygame.K_RETURN]:
            return 'idle'

