# scrolling.py

"""Class to control scrolling of screens"""

import pygame
from copy import deepcopy
import asteroid
import wall

class Scroller(object):
    # constants for screen 'scrolling'
    TOP = 1
    BOTTOM = 2
    LEFT = 3
    RIGHT = 4
    
    def __init__(self, game, level):
        self.game = game
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
        
        print 'Reset! : box is {0}{0}'.format(self.curbox[0], self.curbox[1])

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
            
        print 'moved to {0}{1}'.format(self.curbox[0],self.curbox[1])

    def get_boxlocs(self):
        d = {}
        for box in self.data['allowedbox']:
            d['{0}{1}'.format(box[0],box[1])] = None
        return d

    def off_screen(self, sprite):
        """Return UP, DOWN, LEFT, RIGHT if sprite is offscreen, or None"""
        #print sprite.rect.left, sprite.rect.right, sprite.rect.top, sprite.rect.bottom
        if (sprite.rect.left > self.game.swidth):
            return Scroller.RIGHT
        elif (sprite.rect.left < 0):
            return Scroller.LEFT
        elif (sprite.rect.top > self.game.sheight):
            return Scroller.BOTTOM
        elif (sprite.rect.top < 0):
            return Scroller.TOP
        return None

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
        print key
        if key in self.boxlocs:
            return True
        return False

    def refresh_spritegroup(self):
        """Keep track of the sprites that need to be on the current screen"""
        
        # NOTE: we can remove a sprite from a sprite group, even if it
        # is not actually in that group (handy).  I.e. the removal has no effect
        self.level.allsprites.empty()
        
        print 'refreshing for box {0}{1}'.format(self.curbox[0],self.curbox[1])
        # rocket
        self.level.allsprites.add(self.game.rocket)
        
        # power bar and gravity bar
        if self.curbox == self.sbox and not self.offstart:
            self.level.allsprites.add(self.game.pbar)
            self.level.allsprites.add(self.game.gbar)
        else:
            self.level.allsprites.remove(self.game.pbar)
            self.level.allsprites.remove(self.game.gbar)

        # moon
        if self.curbox == self.ebox:
            self.level.allsprites.add(self.game.moon)
        else:
            self.level.allsprites.remove(self.game.moon)

        # asteroids
        boxkey = '{0}{0}'.format(self.curbox[0], self.curbox[1])
        if boxkey in self.data['asteroids']:
            # create new asteroids and add to the sprite group
            for roidpos in self.data['asteroids'][boxkey]:
                # get positions in pixels!
                posx = roidpos[0]*self.game.swidth
                posy = roidpos[1]*self.game.sheight
                print 'roid at {0},{1}!'.format(posx, posy)

                # create new asteroid and add to both groups
                ast = asteroid.Asteroid((posx,posy))
                self.level.roidsprites.add(ast)
                self.level.allsprites.add(ast)

        # walls for this screen
        leftkey = [self.curbox[0] - 1, self.curbox[1]]
        rightkey = [self.curbox[0] + 1, self.curbox[1]]
        topkey = [self.curbox[0], self.curbox[1] + 1]
        bottomkey = [self.curbox[0], self.curbox[1] - 1]

        if leftkey not in self.data['allowedbox']:
            # add left wall to sprite group
            w = wall.SideWall(self.game.sheight, (0,0))
            self.level.allsprites.add(w)
        if rightkey not in self.data['allowedbox']:
            # add right wall to sprite group
            w = wall.SideWall(self.game.sheight,
                              (self.game.swidth - wall.THICKNESS, 0))            
            self.level.allsprites.add(w)
        if topkey not in self.data['allowedbox']:
            # add top wall to sprite group
            w = wall.TopWall(self.game.swidth, (0, 0))
            self.level.allsprites.add(w)
        if bottomkey not in self.data['allowedbox']:
            # add bottom wall to sprite group
            w = wall.TopWall(self.game.swidth,
                             (0, self.game.sheight - wall.THICKNESS))
            self.level.allsprites.add(w)

    def handle_offscreen(self):

        diroff = self.off_screen(self.game.rocket)

        # if the rocket went off screen, check if we are
        # allowed to go this direction!
        if diroff:
            if self.allowed(diroff):
                print 'moved box!'
                # move the rocket to this position
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
                # the rocket 'died' (crashed off the screen)
                self.game.rktdead = True
                self.reset()

    def update(self):

        # check if the rocket went off the screen
        self.handle_offscreen()

        # check for collision with asteroids, use scaled rects
        if pygame.sprite.spritecollide(self.game.rocket , self.level.roidsprites,
                                       False, self.level.collide_roid):
            self.game.hitasteroid = True
            self.reset()
        
        # if we are in the end box, check if the rocket hit the moon!                
        if self.curbox == self.ebox:                
            if self.level.collide_moon(self.game.rocket, self.game.moon):
                self.game.hitmoon = True
                self.level.finished = True
