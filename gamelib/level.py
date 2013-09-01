import pygame
import sys
import leveldata
import const
from copy import deepcopy

class Level(object):
    # constants for screen 'scrolling'
    TOP = 1
    BOTTOM = 2
    LEFT = 3
    RIGHT = 4
    
    def __init__(self, game, lnum):
        self.game = game
        self.lnum = lnum

        self.data = leveldata.ALLDATA[lnum]
        self.sbox = list(self.data['startbox'])
        self.ebox = list(self.data['endbox'])

        # box location keys, for quick collision checking
        self.boxlocs = self.get_boxlocs()

        # current box = start box (list so that we can assign to it)
        self.curbox = deepcopy(self.sbox)
        
        # this stores all sprites currently on the screen
        self.allsprites = pygame.sprite.RenderUpdates()

        # we always have the rocket!
        self.allsprites.add(self.game.rocket)
        self.allsprites.add(self.game.pbar)
        self.allsprites.add(self.game.gbar)

        # need this in game since we need to access them from elsewhere...
        self.game.hitmoon = False
        self.game.rktdead = False

    def get_boxlocs(self):
        d = {}
        for x in range(self.sbox[0], self.ebox[0] + 1):
            for y in range(self.sbox[0], self.ebox[1] + 1):
                d['{0}{1}'.format(x, y)] = None
        print d
        return d

    def refresh_spritegroup(self):
        """Keep track of the sprites that need to be on the current screen"""
        if self.curbox == self.sbox:
            self.allsprites.add(self.game.pbar)
            self.allsprites.add(self.game.gbar)
        else:
            if self.game.pbar in self.allsprites:
                self.allsprites.remove(self.game.pbar)
                self.allsprites.remove(self.game.gbar)
            if self.curbox == self.ebox:
                self.allsprites.add(self.game.moon)

    def allowed(self, direction):
        """Return if we are allowed to move in a certain direction"""
        if direction == Level.RIGHT:
            key =  '{0}{1}'.format(self.curbox[0] + 1, self.curbox[1])
        elif direction == Level.LEFT:
            key =  '{0}{1}'.format(self.curbox[0] - 1, self.curbox[1])            
        elif direction == Level.BOTTOM:
            key =  '{0}{1}'.format(self.curbox[0], self.curbox[1] - 1)            
        elif direction == Level.TOP:
            key =  '{0}{1}'.format(self.curbox[0], self.curbox[1] + 1)
        print key
        if key in self.boxlocs:
            return True
        return False

    def off_screen(self, sprite):
        """Return UP, DOWN, LEFT, RIGHT if sprite is offscreen, or None"""
        #print sprite.rect.left, sprite.rect.right, sprite.rect.top, sprite.rect.bottom
        if (sprite.rect.left > self.game.swidth):
            return Level.RIGHT
        elif (sprite.rect.right < 0):
            return Level.LEFT
        elif (sprite.rect.bottom > self.game.sheight):
            return Level.BOTTOM
        elif (sprite.rect.top < 0):
            return Level.TOP
        return None

    def main(self):
    
        # main loop
        while True:
            dt = self.game.clock.tick(const.FPS)
            
            # handle events
            self.game.pressed = pygame.key.get_pressed()

            # we are interested in the up and down buttons being
            # released
            self.game.keyup = {}

            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    pygame.quit()
                    sys.exit()
                if event.type == pygame.KEYUP:
                    self.game.keyup[event.key] = True

            # check if the rocket went off the screen
            diroff = self.off_screen(self.game.rocket)

            # get the correct sprites in self.allsprites
            self.allsprites.clear(self.game.screen, self.game.background)            

            # if the rocket went off screen, check if we are
            # allowed to go this direction!
            if diroff:
                if self.allowed(diroff):
                    # move the rocket to this position
                    if diroff == Level.RIGHT:
                        self.game.rocket.rect.centerx -= self.game.swidth
                        self.curbox[0] += 1
                    if diroff == Level.LEFT:
                        self.game.rocket.rect.centerx += self.game.swidth
                        self.curbox[0] -= 1                        
                    if diroff == Level.TOP:
                        self.game.rocket.rect.centery += self.game.sheight
                        self.curbox[1] += 1                                                
                    if diroff == Level.BOTTOM:
                        self.game.rocket.rect.centery -= self.game.sheight
                        self.curbox[1] -= 1
                        # since we moved screen, refresh spritegroup
                    self.refresh_spritegroup()
                else:
                    self.game.rktdead = True
                    self.curbox = deepcopy(self.sbox)
                    print self.curbox, self.sbox
            #print self.curbox
            if self.curbox == self.ebox:                
                # check if the rocket hit the moon!                
                if pygame.sprite.collide_rect(self.game.rocket, self.game.moon):
                    self.game.hitmoon = True

            # update sprites
            self.allsprites.update(dt/1000.0, self.game)

            # render our sprites
            dirty = self.allsprites.draw(self.game.screen)
            pygame.display.update(dirty)
