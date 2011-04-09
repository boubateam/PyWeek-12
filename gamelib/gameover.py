'''The game over scene.
'''

import pygame
import scene
import data
import string
import os

class GameOverScene(scene.Scene):
    def __init__(self, game, name, index, config=None):
        super(GameOverScene, self).__init__(game, name, index, config)

        gameovermessage = config['message'] if 'message' in config else 'Game Over'
        gameovermusic = config['music'] if 'music' in config else 'gameover.ogg'

        self.gameovertxt = data.render_text(data.FONT_TITLE, 30, gameovermessage, (255, 255, 255))
        self.gameovertxtRect = self.gameovertxt.get_rect()
        self.background = data.load_image('gameover.png')

        self.music_bg = data.load_sound(gameovermusic)

        self.teaserText = data.render_text(data.FONT_MAIN, 17, 'Who\'s the rockstar with '+str(self.game.points)+' points ?', (255, 255, 255))
        self.teaserTextrect = self.teaserText.get_rect()

        #temp
        self.teaserTextInputRect = self.teaserTextrect
        self.blinkInputCounter = 0
        self.blinkInputTime = 400
        self.userFilledStr = []
        self.usernickText = None
        self.usernickTextRect = None
        self.userFillingTextField = True
        self.showUnderscore = True
        self.lScoreFile = None
        self.userscores = None
        self.orderedTabScore = []
        self.buildTabScore()
        
    def buildTabScore(self):
        self.lScoreFile = open(data.filepath('topscore.txt'), 'r')
        self.userscores = self.lScoreFile.readlines()
        self.lScoreFile.close()
        self.orderedTabScore = []
        
        for i in self.userscores:
            curinfo = i.partition('-')
            self.orderedTabScore.append((int(curinfo[0]), curinfo[2].strip()))
            
        self.orderedTabScore.sort(reverse=True)
        
    def start(self):
        self.music_bg.play()

    def end(self):
        self.music_bg.fadeout(1000)    

    def handleEvent(self, event):
        if event.type == pygame.MOUSEBUTTONUP:
            if self.teaserTextInputRect.collidepoint(event.pos):
                self.userFillingTextField = True
        
        if event.type == pygame.KEYDOWN:
            llen = len(self.userFilledStr)
            if llen > 0 and self.userFilledStr[llen-1] ==  '_':
                 self.userFilledStr = self.userFilledStr[0:-1]

            if not self.userFillingTextField and event.key in [ pygame.K_ESCAPE, pygame.K_RETURN, pygame.K_SPACE]:
                self.game.director.change('menu')
            elif self.userFillingTextField and event.key == pygame.K_ESCAPE:
                self.game.director.change('menu')
            
            if self.userFillingTextField:
                #if event.key == pygame.K_ENTER:
                if event.key == pygame.K_BACKSPACE:
                    self.userFilledStr = self.userFilledStr[0:-1]

                elif event.key == pygame.K_RETURN:                    
                    self.userFillingTextField = False
                    self.saveUserName()
                elif event.key <= 127 and event.key >= 97:
                    self.userFilledStr.append(chr(event.key))

    def update(self):
        if self.userFillingTextField :
            llen = len(self.userFilledStr)
    
            if self.showUnderscore and (llen==0 or self.userFilledStr[llen-1] !=  '_'):
                self.userFilledStr.append('_')
            elif llen>0  and self.showUnderscore == False:
                if self.userFilledStr[llen-1] == '_':
                    self.userFilledStr.pop()
                        
        self.gameovertxtRect.center = (320, 20)
        self.usernickText = data.render_text(data.FONT_TITLE, 17, "".join(self.userFilledStr), (255, 255, 255))
        self.usernickTextRect = self.usernickText.get_rect()
        self.teaserTextrect.center = (320, 50)
        self.usernickTextRect.center = (320, 70)

        if pygame.time.get_ticks() > self.blinkInputCounter :
            self.blinkInputCounter = pygame.time.get_ticks()+self.blinkInputTime
            self.showUnderscore = not self.showUnderscore 

    def draw(self, screen):
        screen.blit(self.background, (0, 0))
        screen.blit(self.gameovertxt, self.gameovertxtRect)

        if self.userFillingTextField :
            screen.blit(self.teaserText, self.teaserTextrect)
            screen.blit(self.usernickText, self.usernickTextRect)
        
        y = 70
        for userPts, username in self.orderedTabScore:
                y+=20
                tabScoreName = data.render_text(data.FONT_TITLE, 17, str(userPts)+"-"+username, (255, 255, 255))
                rect = tabScoreName.get_rect()
                rect.center = (320, y)
                screen.blit(tabScoreName,rect)

    def saveUserName(self):
        self.lScoreFile = open(data.filepath('topscore.txt'), 'a+')
        lstr = "".join(self.userFilledStr)
        self.lScoreFile.write(str(self.game.points)+"-"+str(lstr.strip())+os.linesep)
        self.lScoreFile.close()
        self.buildTabScore()