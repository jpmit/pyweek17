# scrolling.py

"""Class to control scrolling of screens"""

import pygame
from copy import deepcopy
import asteroid
import wall
import fontsprite
import const

class Scroller(object):
    # constants for screen 'scrolling'
    TOP = 1
    BOTTOM = 2
    LEFT = 3
    RIGHT = 4
    
    def __init__(self, game):
        self.game = game

    def new_level(self, level):
        """Call this at the start of every new level."""
        self.level = level        
        self.data = level.data

        # start box (where rocket is launched from) and end box (where
        # moon is) in (normal) Cartesian coords.
        self.sbox = self.data['startbox']
        self.ebox = self.data['endbox']

        # box location keys, for quick checking of whether we are
        # allowed to scroll to a consecutive box.
        self.boxlocs = self.get_boxlocs()

        # set current box = start box (list so that we can assign to it)
        self.reset()

    def reset(self):
        """Go back to the start box"""
        self.lastbox = deepcopy(self.sbox)
        self.curbox = deepcopy(self.sbox)
        self.offstart = False # has the rocket left the start box?

        self.refresh_spritegroup()

    def move_box(self, direction):
        if self.curbox == self.sbox:
            self.offstart = True
        if direction == Scroller.TOP:
            self.curbox[1] += 1
        elif direction == Scroller.BOTTOM:
            self.curbox[1] -= 1
        if direction == Scroller.LEFT:
            self.curbox[0] -= 1
        if direction == Scroller.RIGHT:
            self.curbox[0] += 1

    def get_boxlocs(self):
        d = {}
        for box in self.data['allowedbox']:
            d['{0}{1}'.format(box[0],box[1])] = None
        return d

    def off_screen(self, sprite):
        """Return UP, DOWN, LEFT, RIGHT if sprite is offscreen, or None"""
        if (sprite.rect.right > self.game.swidth):        
            return Scroller.RIGHT
        elif (sprite.rect.left < 0):
            return Scroller.LEFT
        elif (sprite.rect.bottom > self.game.sheight):        
            return Scroller.BOTTOM
        elif (sprite.rect.top < 0):
            return Scroller.TOP
        return None

    def need_scroll(self, direction):
        if (direction == Scroller.TOP or
            direction == Scroller.LEFT):
            return True
        if (direction == Scroller.RIGHT):
            return (self.game.rocket.rect.left > self.game.swidth)
        elif (direction == Scroller.BOTTOM):
            return (self.game.rocket.rect.top > self.game.sheight)

    def allowed(self, direction):
        """Return if we are allowed to move in a certain direction"""
        if direction == Scroller.RIGHT:
            key =  '{0}{1}'.format(self.curbox[0] + 1, self.curbox[1])
        elif direction == Scroller.LEFT:
            key =  '{0}{1}'.format(self.curbox[0] - 1, self.curbox[1])
            
        elif direction == Scroller.BOTTOM:
            key =  '{0}{1}'.format(self.curbox[0], self.curbox[1] - 1)
            
        elif direction == Scroller.TOP:
            key =  '{0}{1}'.format(self.curbox[0], self.curbox[1] + 1)

        if key in self.boxlocs:
            return True
        return False

    def refresh_spritegroup(self):
        """Keep track of the sprites that need to be on the current
        screen"""
        
        # NOTE: we can remove a sprite from a sprite group, even if it
        # is not actually in that group (handy).  I.e. the removal has
        # no effect
        self.level.allsprites.empty()
        self.level.roidsprites.empty()

        # level text
        self.level.allsprites.add(self.level.ltext)
        self.level.allsprites.add(self.game.destroyedtext)        
        
        # power bar and gravity bar
        if self.curbox == self.sbox and not self.offstart:
            self.level.allsprites.add(self.game.pbar)
            self.level.allsprites.add(self.game.gbar)
            self.level.allsprites.add(self.game.pbartext)
            self.level.allsprites.add(self.game.gbartext)            
        else:
            self.level.allsprites.remove(self.game.pbar)
            self.level.allsprites.remove(self.game.gbar)
            self.level.allsprites.remove(self.game.pbartext)
            self.level.allsprites.remove(self.game.gbartext)

        # moon
        if self.curbox == self.ebox:
            self.level.allsprites.add(self.game.moon)
        else:
            self.level.allsprites.remove(self.game.moon)

        # asteroids
        boxkey = '{0}{1}'.format(self.curbox[0], self.curbox[1])
        if boxkey in self.data['asteroids']:
            # create new asteroids and add to the sprite group
            for roidpos in self.data['asteroids'][boxkey]:
                # get positions in pixels!
                posx = roidpos[0]*self.game.swidth
                posy = roidpos[1]*self.game.sheight
                ast = asteroid.Asteroid(self.game, (posx,posy))
                # create new asteroid and add to both groups
                self.level.roidsprites.add(ast)
                self.level.allsprites.add(ast)

        # walls for this screen
        leftkey = [self.curbox[0] - 1, self.curbox[1]]
        rightkey = [self.curbox[0] + 1, self.curbox[1]]
        topkey = [self.curbox[0], self.curbox[1] + 1]
        bottomkey = [self.curbox[0], self.curbox[1] - 1]

        # add wall or arrow on each of the 4 edges of the screen
        # left
        if leftkey not in self.data['allowedbox']:
            self.level.allsprites.add(self.level.lwall)            
        else:
            self.level.larrow.reset()
            self.level.allsprites.add(self.level.larrow)
        # right
        if rightkey not in self.data['allowedbox']:
            self.level.allsprites.add(self.level.rwall)
        else:
            # add arrow to the right
            self.level.rarrow.reset()            
            self.level.allsprites.add(self.level.rarrow)
        # top
        if topkey not in self.data['allowedbox']:
            self.level.allsprites.add(self.level.uwall)
        else:
            self.level.uarrow.reset()            
            self.level.allsprites.add(self.level.uarrow)
        # bottom
        if bottomkey not in self.data['allowedbox']:
            self.level.allsprites.add(self.level.dwall)
        else:
            self.level.darrow.reset()                        
            self.level.allsprites.add(self.level.darrow)

        # rocket
        self.level.allsprites.add(self.game.rocket)

    def handle_offscreen(self):

        diroff = self.off_screen(self.game.rocket)

        # if the rocket went off screen, check if we are
        # allowed to go this direction!
        if diroff:
            if self.allowed(diroff):
                # check if we need to scroll
                if self.need_scroll(diroff):
                    # move the rocket to this position and set the box
                    if diroff == Scroller.RIGHT:
                        self.game.rocket.rect.centerx -= self.game.swidth
                        self.move_box(diroff)
                    if diroff == Scroller.LEFT:
                        self.game.rocket.rect.centerx += self.game.swidth
                        self.move_box(diroff)                    
                    if diroff == Scroller.TOP:
                        self.game.rocket.rect.centery += self.game.sheight 
                        self.move_box(diroff)                    
                    if diroff == Scroller.BOTTOM:
                        self.game.rocket.rect.centery -= self.game.sheight
                        self.move_box(diroff)

                    # get the sprites for this new box
                    self.refresh_spritegroup()
            else:
                if not const.GODMODE:
                    # the rocket 'died' (crashed off the screen)
                    self.game.sfx['error'].play()
                    self.game.rktdead = True
                    self.game.numdestroyed += 1
                    self.game.destroyedtext.set_text('{0}{1}'.\
                                                     format(fontsprite.DTEXT,
                                                            self.game.numdestroyed))
                    self.reset()

    def update(self):

        # check if the rocket went off the screen
        self.handle_offscreen()

        # check for collision with asteroids, use scaled rects
        if pygame.sprite.spritecollide(self.game.rocket , self.level.roidsprites,
                                       False, self.game.collide_roid):
            self.game.hitasteroid = True
        
        # if we are in the end box, check if the rocket hit the moon!                
        if self.curbox == self.ebox:                
            if self.game.collide_moon(self.game.rocket, self.game.moon):
                self.game.hitmoon = True

        # make sure we go back to the start screen if we hit an
        # asteroid and reset hit status
        if (self.game.hitasteroid and
            self.game.rocket.brain.get_state() == 'onlaunchpad'):
            self.game.hitasteroid = False
            self.reset()

        if (self.game.hitmoon and
            self.game.rocket.brain.get_state() == 'onlaunchpad'):
            self.level.hitmoon = False
            self.level.finished = True
