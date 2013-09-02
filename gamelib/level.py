# level.py

import pygame
import sys
import leveldata
import scrolling
import const

class Level(object):
    CRECTROID = 0.5 # for asteroid
    CRECTMOON = 0.8 # for moon
    def __init__(self, game, lnum):
        self.game = game
        self.lnum = lnum

        self.data = leveldata.ALLDATA[lnum]
        
        # this stores all sprites currently on the screen
        self.allsprites = pygame.sprite.RenderUpdates()

        # this stores only asteroid sprites for collision checking
        self.roidsprites = pygame.sprite.Group()

        # we always have the rocket!
        self.allsprites.add(self.game.rocket)

        # scroller handles moving screen and sprites etc
        self.scroller = scrolling.Scroller(self.game, self)

        # collision function for checking collisions between asteroids
        # and rocket
        self.collide_roid = pygame.sprite.collide_rect_ratio(Level.CRECTROID)
        self.collide_moon = pygame.sprite.collide_rect_ratio(Level.CRECTMOON)

        # put the moon in the right place
        self.game.moon.set_pos((self.data['moonpos'][0]*self.game.swidth,
                                self.data['moonpos'][1]*self.game.sheight))

        # put moon and rocket in start state
        self.game.moon.set_start_state()
        self.game.rocket.set_start_state()
        self.game.pbar.set_start_state()
        self.game.gbar.set_start_state()

        self.game.hitmoon = False
        self.finished = False

        # blit background onto screen
        self.game.screen.blit(self.game.background, (0,0))
        pygame.display.update()

    def store_events(self):
        # store pressed keys in game so that rocket etc. can access
        self.game.pressed = pygame.key.get_pressed()

        # store up and down buttons being released for gravity bar
        self.game.keyup = {}

        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                sys.exit()
            if event.type == pygame.KEYUP:
                self.game.keyup[event.key] = True

    def main(self):
    
        # main loop
        while True:
            dt = self.game.clock.tick(const.FPS)

            # store any user input for use in updating the sprites
            self.store_events()

            # get the correct sprites in self.allsprites
            self.allsprites.clear(self.game.screen, self.game.background)

            # update the scroller -> see if rocket went off-screen and
            # handle appropriately.  This also adds/removes from the
            # group self.allsprites.
            self.scroller.update()

            # update sprites
            self.allsprites.update(dt/1000.0, self.game)

            # render our sprites
            dirty = self.allsprites.draw(self.game.screen)
            pygame.display.update(dirty)

            if self.finished: # this is very hacky
                # remove all sprites
                print 'finished level'
                return
