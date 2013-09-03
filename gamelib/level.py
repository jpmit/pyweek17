# level.py

import pygame
import sys
import leveldata
import scrolling
import const
import fontsprite
import wall

class Level(object):
    
    def __init__(self, game, lnum):
        self.game = game
        self.lnum = lnum

        self.data = leveldata.ALLDATA[lnum]
        
        # this stores all sprites currently on the screen
        self.allsprites = pygame.sprite.RenderUpdates()

        # this stores only asteroid sprites for collision checking
        self.roidsprites = pygame.sprite.Group()

        # some sprites: walls and arrows
        self.larrow = wall.Arrow(wall.Arrow.LEFT)
        self.uarrow = wall.Arrow(wall.Arrow.UP)
        self.rarrow = wall.Arrow(wall.Arrow.RIGHT)
        self.darrow = wall.Arrow(wall.Arrow.DOWN)

        self.lwall = wall.SideWall(self.game.sheight, (0,0))        
        self.uwall = wall.TopWall(self.game.swidth, (0, 0))
        self.dwall = wall.TopWall(self.game.swidth,
                                  (0, self.game.sheight - wall.THICKNESS))
        self.rwall = wall.SideWall(self.game.sheight,
                                   (self.game.swidth - wall.THICKNESS, 0))        
        
        # initialise level - put everything in the right place etc.
        self.init_level()

    def init_level(self):
        # menu font
        self.ltext = fontsprite.LevelText(self.game.levelfont, self.lnum + 1)

        # initialize scroller which handles screen movement
        self.game.scroller.new_level(self)

        # put the moon in the right place
        self.game.moon.set_pos((self.data['moonpos'][0]*self.game.swidth,
                                self.data['moonpos'][1]*self.game.sheight))

        # put moon, rocket and power gauges in start state
        self.game.moon.set_start_state()
        self.game.rocket.set_start_state()
        self.game.pbar.set_start_state()
        self.game.gbar.set_start_state()

        self.game.hitasteroid = False
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
        while not self.finished:
            dt = self.game.clock.tick(const.FPS)

            # store any user input for use in updating the sprites
            self.store_events()

            # get the correct sprites in self.allsprites
            self.allsprites.clear(self.game.screen,
                                  self.game.background)

            # update the scroller -> see if rocket went off-screen and
            # handle appropriately.  This also adds/removes from the
            # group self.allsprites.
            self.game.scroller.update()

            # update sprites
            self.allsprites.update(dt/1000.0, self.game)

            # render our sprites
            dirty = self.allsprites.draw(self.game.screen)
            pygame.display.update(dirty)

        # if here, we have finished the level, do any cleanup.
