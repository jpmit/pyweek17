import pygame
import data
import const

class Powerbar(pygame.sprite.Sprite):
    def __init__(self):
        super(Powerbar, self).__init__()
        self.image = pygame.Surface((300,80))
        self.image.fill(const.WHITE)

        self.rect = pygame.draw.rect(self.image, const.BLACK,
                                     self.image.get_rect(), 1)
        
        # have we started the launch procedure (i.e. pressed space)
        self.inlaunch = False
        self.rect = self.image.get_rect()


        # orientation angle to vertical (clockwise in degrees)
        self.oangle = 0.0

        # fill with a bit of red
        redrect = self.rect
        redrect.width = 100
        self.image.fill(const.RED, redrect)

        self.rect.centerx, self.rect.centery = (500,500)

    def update(self, dt, game):
        if game.pressed[pygame.K_SPACE]:
            # add some red to the status bar image
            pass

class Rocket(pygame.sprite.Sprite):
    def __init__(self, xy):
        super(Rocket, self).__init__()
        self.baseimage = pygame.image.load(data.filepath('rocket.png')).\
                         convert_alpha()
        self.image = self.baseimage
        self.rect = self.image.get_rect()

        self.rect.centerx, self.rect.centery = xy

        # orientation angle to vertical (clockwise in degrees)
        self.oangle = 0.0

    def update(self, dt, game):
        # save old coordinates and old orientation angle
        ox, oy = self.rect.centerx, self.rect.centery
        oa = self.oangle

        if game.pressed[pygame.K_RIGHT]:
            # if we are pressing button, update orientation angle
            self.oangle -= dt*10.0
        if game.pressed[pygame.K_LEFT]:
            self.oangle += dt*10.0

        if self.oangle != oa:
            # we want to rotate the image
            self.image = pygame.transform.rotate(self.baseimage, self.oangle)
            self.rect = self.image.get_rect()
            self.rect.centerx = ox
            self.rect.centery = oy

class Moon(pygame.sprite.Sprite):
    def __init__(self, xy):
        super(Moon, self).__init__()
        self.image = pygame.Surface((80,80))
        srect = self.image.get_rect()
        self.rect = pygame.draw.circle(self.image, const.WHITE,
                                        (srect.centerx,
                                        srect.centery), 40)
        self.rect.centerx, self.rect.centery = xy        

    def update(self, dt, game):

        #self.rect.right += dt*200
        pass
