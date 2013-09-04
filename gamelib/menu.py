import pygame
import sys
import const
import data

NEWGAME = 0
LEVEL = 1
HELP = 2
SELCOL = const.GBARCOLOR # same color as gravity bar

class Menu(object):
    # positions are top left of rect
    NEWPOS = (300, 150)
    LEVELPOS = (300, 250)        
    HELPPOS = (300, 350)
    ROCKETPOS = (80, 40)
    def __init__(self, game):
        self.game = game
        self.screen = self.game.screen

        # background
        self.background = self.game.background

        # rocket
        self.rocket = pygame.image.load(data.filepath('rocket.png')).\
                      convert_alpha()

        # the selected option
        self.selected = NEWGAME
        
        self.newgame = self.game.menufont.render('NEW GAME', True,
                                                 const.WHITE)
        self.newgame_sel = self.game.menufont.render('NEW GAME', True,
                                                 SELCOL)

        self.level =  self.game.menufont.render('LEVEL SELECT', True,
                                                const.WHITE)
        self.level_sel =  self.game.menufont.render('LEVEL SELECT', True,
                                                    SELCOL)        

        self.help = self.game.menufont.render('HELP', True,
                                              const.WHITE)
        self.help_sel = self.game.menufont.render('HELP', True,
                                                  SELCOL)

        # the actual text of the help menu
        help = [ 'up and down arrow keys',
                 'to adjust gravity level',
                '',
                'left and right arrow keys',
                'to aim rocket',
                '',
                'press and hold spacebar',
                'to fire rocket',
                '',
                'Reach the moon',
                 'to complete the level!'
                ]
        self.helptext = [self.game.helpfont.render(h, True, const.WHITE)
                         for h in help]
        
        self.selected = NEWGAME
        self.exit = False
        self.helpon = False
        self.levelon = False
        self.levselected = 0        

    def draw_help_text(self):
        ROOTPOS = (300, 80)
        YSPACE = 40
        for (i,h) in enumerate(self.helptext):
            self.screen.blit(h, (ROOTPOS[0],ROOTPOS[1] + i*YSPACE))

    def draw_level_text(self):
        ROOTPOS = (300, 80)
        YSPACE = 40
        nlev = self.game.numlevels
        lev = ['{0}'.format(i + 1) for i in range(nlev)]
        levtext = []
        for (i, lt) in enumerate(lev):
            if i == self.levselected:
                levtext.append(self.game.helpfont.render(lt, True, SELCOL))
            else:
                levtext.append(self.game.helpfont.render(lt, True, const.WHITE))

        for (i,h) in enumerate(levtext):
            self.screen.blit(h, (ROOTPOS[0], ROOTPOS[1] + i*YSPACE))

    def draw_text(self):
        if self.helpon:
            self.draw_help_text()
        elif self.levelon:
            self.draw_level_text()
        else:
            if self.selected == NEWGAME:
                self.screen.blit(self.newgame_sel, Menu.NEWPOS)
                self.screen.blit(self.level, Menu.LEVELPOS)                                
                self.screen.blit(self.help, Menu.HELPPOS)
            elif self.selected == LEVEL:
                self.screen.blit(self.newgame, Menu.NEWPOS)
                self.screen.blit(self.level_sel, Menu.LEVELPOS)                                
                self.screen.blit(self.help, Menu.HELPPOS)
            elif self.selected == HELP:
                self.screen.blit(self.newgame, Menu.NEWPOS)
                self.screen.blit(self.level, Menu.LEVELPOS)                                                
                self.screen.blit(self.help_sel, Menu.HELPPOS)

    def sel_up(self):
        if not self.helpon:
            self.game.sfx['click'].play()
        # are we on the level select screen?
        if self.levelon:
            self.levselected -= 1
            if self.levselected < 0:
                self.levselected = self.game.numlevels - 1
        else:
            if self.selected == NEWGAME:
                self.selected = HELP
            elif self.selected == LEVEL:
                self.selected = NEWGAME
            elif self.selected == HELP:
                self.selected = LEVEL

    def sel_down(self):
        if not self.helpon:
            self.game.sfx['click'].play()
        # are we on the level select screen?
        if self.levelon:
            self.levselected += 1
            if self.levselected > self.game.numlevels - 1:
                self.levselected = 0
        else:
            if self.selected == NEWGAME:
                self.selected = LEVEL
            elif self.selected == LEVEL:
                self.selected = HELP
            elif self.selected == HELP:
                self.selected = NEWGAME

    def handle_return_down(self):
        if self.selected == NEWGAME or self.levelon:
            self.exit = True

    def handle_return_up(self):
        if self.selected == HELP:
            # turn help on/off
            self.helpon = not self.helpon
        elif self.selected == LEVEL:
            self.levelon = not self.levelon

    def start(self):
        while not self.exit:
            self.game.clock.tick(const.FPS)
            
            self.screen.blit(self.background, (0, 0))
            self.screen.blit(self.rocket, Menu.ROCKETPOS)            
            self.draw_text()

            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    pygame.quit()
                    sys.exit()
                elif event.type == pygame.KEYDOWN:
                    if (event.key == pygame.K_DOWN):
                        self.sel_down()
                    elif (event.key == pygame.K_UP):
                        self.sel_up()
                    if event.key == pygame.K_RETURN:
                        self.handle_return_down()
                elif event.type == pygame.KEYUP:
                    if event.key == pygame.K_RETURN:
                        self.handle_return_up()

            pygame.display.update()

        # return the level selected
        return self.levselected

    def draw_end_text(self):
        ndest = self.game.numdestroyed
        
        if ndest < 10:
            name = 'STAR SEEKER'
            # line of text list below to highlight
            hlt = 5
        elif ndest < 100:
            name = 'ASTRONAUT'
            hlt = 6            
        elif ndest < 1000:
            name = 'SPACE MONKEY'
            hlt = 7                        
        else:
            name = 'COSMIC FAILURE'
            hlt = 8            

        text = ['GAME COMPLETE!',
                '',
                '',
                'ROCKETS DESTROYED: {0}'.format(ndest),
                '',
                '0-9:      STAR SEEKER',
                '10-99:    ASTRONAUT',
                '100-999: SPACE MONKEY',
                '1000+:    COSMIC FAILURE']
        scoretext = []
        for (i, s) in enumerate(text):
            if i == hlt:
                col = SELCOL
            else:
                col = const.WHITE
                
            scoretext.append(self.game.helpfont.render(s, True, col))

        # draw the actual text
        ROOTPOS = (280, 80)
        YSPACE = 40
        for (i, s) in enumerate(scoretext):
            self.screen.blit(s, (ROOTPOS[0], ROOTPOS[1] + i*YSPACE))

    def finish(self):
        print 'finished game!!!'        
        # We have completed the game.  Say something nice to the player.
        # figure out what I am from how many rockets I destroyed.

        # blit the text to the screen,
        self.screen.blit(self.background, (0, 0))
        self.draw_end_text()
        pygame.display.update()
        
        # wait for return key
        ex = False
        while not ex:
            for event in pygame.event.get():
                if ((event.type == pygame.KEYUP) and
                    (event.key == pygame.K_RETURN)):
                    ex = True
                if event.type == pygame.QUIT:
                    pygame.quit()
                    sys.exit()                    
                
            self.game.clock.tick(const.FPS)

        # stop the music
        pygame.mixer.music.stop()
        
        # reset exit status for next play!
        self.exit = False
        self.levelon = False
        self.selected = NEWGAME
