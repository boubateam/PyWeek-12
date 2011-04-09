'''The intro scene.

04/04/2011 : add sound
'''

import pygame
import scene
import data

class IntroScene(scene.Scene):
    def __init__(self, game, name, index, config=None):
        super(IntroScene, self).__init__(game, name, index, config)

        self.background = data.load_image('intro.png')
        self.music = data.load_sound('intro.ogg')

        self.endTime = None
        self.currentIntroIdx = None
        self.intros = []
        self.intros.append(Intro(5000, True, ['2038. The Earth.', 'Sonore Aliens wade in !', 'With their ultrasonic sounds', 'they want to destroy humanity !']))
        self.intros.append(Intro(7000, True, ['Thanks to', 'the found sumerian technology', 'dated 4000 years BC', 'human resistance can recreate', 'sonore attacks and defend the Earth.', '', 'Fight for the resistance !']))
        
        self.blinkText = None
        self.blinkTextRect = None
        self.blinkInputCounter = 0
        self.blinkInputTime = 500
        self.showBlinkText = True

    def start(self):
        #Blink text
        self.blinkText = data.render_text(data.FONT_MAIN, 15, '(Press SPACE to skip)', (51, 204, 0))
        self.blinkTextRect = self.blinkText.get_rect()
        self.blinkTextRect.center = (320, 30)
        self.blinkTextRect.top = 430
        
        #music
        self.game.channel = self.game.music.play(-1, fade_ms=4000)
        
        #which intro
        self.currentIntroIdx = 0
        self.endTime = pygame.time.get_ticks() + self.intros[0].duration

    def end(self):
        pass

    def handleEvent(self, event):
        if event.type == pygame.KEYDOWN:
            if event.key == pygame.K_ESCAPE: 
                self.game.director.endScene()
            elif event.key == pygame.K_SPACE and self.intros[self.currentIntroIdx].canPass:
                self.nextIntro()
        elif event.type == pygame.MOUSEBUTTONUP:
            self.game.director.endScene()
            
    def nextIntro(self):
        if self.currentIntroIdx + 1 < len(self.intros):
            self.currentIntroIdx += 1
            self.endTime = pygame.time.get_ticks() + self.intros[self.currentIntroIdx].duration
        else:
            self.game.director.endScene()

    def update(self):
        if pygame.time.get_ticks() > self.endTime:
            self.nextIntro()
        
        if pygame.time.get_ticks() > self.blinkInputCounter :
            self.blinkInputCounter = pygame.time.get_ticks()+self.blinkInputTime
            self.showBlinkText = not self.showBlinkText 

    def draw(self, screen):
        currIntro = self.intros[self.currentIntroIdx]
        currIntroRect = currIntro.get_rect()
        currIntroRect.center = (320, 240)

        screen.blit(self.background, (0, 0))
        screen.blit(currIntro, currIntroRect)
        
        if self.showBlinkText:
            screen.blit(self.blinkText, self.blinkTextRect)

class Intro(pygame.surface.Surface):
    def __init__(self, duration, canPass, text, textsize = 25):
        pygame.surface.Surface.__init__(self, (550, 380), flags=pygame.SRCALPHA)
        self.duration = duration
        self.canPass = canPass

        # Include texts into content
        tmpContent = None
        top = 0
        for partText in text:
            tmpContent = data.render_text(data.FONT_MAIN, textsize, partText, (255, 255, 255))
            tmpSize = tmpContent.get_rect()
            tmpSize.centerx = self.get_rect().centerx
            tmpSize.top = top
            self.blit(tmpContent, tmpSize)
            top = top + tmpSize.height * 1.5
