import state
import pygame
import const

# constants for positioning the font sprites I use in the game
LEVLOC = (50, 20)
PBARLOC = (180, 510)
DESTLOC = (50, 60)
GBARLOC = (428, 455)
DTEXT = 'ROCKETS DESTROYED: '

class FontSprite(state.BaseSprite):
    def __init__(self, font, text, pos):
        super(FontSprite, self).__init__()

        self.font = font

        # pos is position of the top left of the rect
        self.pos = pos

        self.set_text(text)

    def set_text(self, text):
        """Render the font, hence setting the image and rect
        attributes."""
        self.image = self.font.render(text, True, const.WHITE)
        self.rect = self.image.get_rect()
        self.rect.topleft = self.pos
