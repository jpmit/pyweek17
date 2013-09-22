import pygame
import data

class Spritesheet(object):
    # This class is based on http://www.pygame.org/wiki/Spritesheet    
    def __init__(self, filename):
        """filename should be a file in data directory"""
        try:
            self.sheet = pygame.image.load(data.filepath(filename)).\
                         convert_alpha()
        except pygame.error, message:
            print 'Unable to load spritesheet image:', filename
            raise SystemExit, message

    def image_at(self, rectangle, colorkey = None):
        "Loads image from x,y,x+offset,y+offset"
        rect = pygame.Rect(rectangle)
        image = pygame.Surface(rect.size, pygame.SRCALPHA,
                               32).convert_alpha()
        image.blit(self.sheet, (0, 0), rect)
        if colorkey is not None:
            if colorkey is -1:
                colorkey = image.get_at((0,0))
            image.set_colorkey(colorkey, pygame.RLEACCEL)
        return image

    def images_at(self, rects, colorkey = None):
        "Loads multiple images, supply a list of coordinates" 
        return [self.image_at(rect, colorkey) for rect in rects]

    def load_strip(self, rect, image_count, colorkey = None):
        "Loads a strip of images and returns them as a list"
        tups = [(rect[0]+rect[2]*x, rect[1], rect[2], rect[3])
                for x in range(image_count)]
        return self.images_at(tups, colorkey)

    def all_images(self, nx, ny, sizex, sizey):
        rects = []
        for i in range(nx):
            for j in range(ny):
                rects.append(pygame.Rect(j*sizex, i*sizey,
                                         sizex, sizey))
        return self.images_at(rects)
