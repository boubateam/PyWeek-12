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
        self.intros.append(Intro(4000, False, ['Welcome to', 'Ninth Kind']))
        self.intros.append(Intro(4000, True, ['Im Evil !', 'Beat Me !', 'Mouhahah !']))

    def start(self):
        self.music.play(-1, fade_ms=4000)
        self.currentIntroIdx = 0
        self.endTime = pygame.time.get_ticks() + self.intros[0].duration

    def end(self):
        self.music.fadeout(2000)

    def handleEvent(self, event):
        if event.type == pygame.KEYDOWN:
            if event.key == pygame.K_ESCAPE:
                self.game.director.endScene()
            elif event.key == pygame.K_SPACE and self.intros[self.currentIntroIdx].canPass:
                self.nextIntro()

    def nextIntro(self):
        if self.currentIntroIdx + 1 < len(self.intros):
            self.currentIntroIdx += 1
            self.endTime = pygame.time.get_ticks() + self.intros[self.currentIntroIdx].duration
        else:
            self.game.director.endScene()

    def update(self):
        if pygame.time.get_ticks() > self.endTime:
            self.nextIntro()
        
    def draw(self, screen):
        currIntro = self.intros[self.currentIntroIdx]
        currIntroRect = currIntro.get_rect()
        currIntroRect.center = (320, 240)
        
        screen.blit(self.background, (0, 0))
        screen.blit(currIntro, currIntroRect)
        
class Intro(pygame.surface.Surface):
    def __init__(self, duration, canPass, text, image=None):
        pygame.surface.Surface.__init__(self, (400, 300), flags=pygame.SRCALPHA)
        self.duration = duration
        self.canPass = canPass
        
        # Include texts into content
        tmpContent = None
        top = 0
        for partText in text:
            tmpContent = data.render_text('genotype.ttf', 30, partText, (255, 255, 255))
            tmpContentRect = tmpContent.get_rect()
            tmpContentRect.center = (400, top)
            self.blit(tmpContent, (0, top))
            top += 30
