'''The intro scene.

04/04/2011 : add sound
'''

import pygame
import scene
import data

class IntroScene(scene.Scene):
    def __init__(self, game, name, index, config=None):
        super(IntroScene, self).__init__(game, name, index, config)

#        self.text = data.render_text('genotype.ttf', 30, 'Ninth Kind', (255, 255, 255))
#        self.textrect = self.text.get_rect()

        self.background = data.load_image('intro.png')
        self.music = data.load_sound('intro.ogg')
        
        self.endTime = None
        self.currentIntroIdx = None
        self.intros = []
        self.intros.append(Intro(4000, ['Welcome to', 'Ninth Mind']))
        self.intros.append(Intro(4000, ['Im Evil !', 'Beat Me !', 'Mouhahah !']))

    def start(self):
        self.music.play(-1, fade_ms=4000)
        self.currentIntroIdx = 0
        self.endTime = pygame.time.get_ticks() + self.intros[0].duration

    def end(self):
        self.music.fadeout(2000)

    def handleEvent(self, event):
        if event.type == pygame.KEYDOWN:
            if event.key == pygame.K_ESCAPE:
                self.game.end()
            elif event.key == pygame.K_SPACE:
                self.game.director.endScene()

    def update(self):
        if pygame.time.get_ticks() > self.endTime:
            if self.currentIntroIdx + 1 < len(self.intros):
                self.currentIntroIdx += 1
                self.endTime = pygame.time.get_ticks() + self.intros[self.currentIntroIdx].duration
            else:
                self.game.director.endScene()

        currIntro = self.intros[self.currentIntroIdx]
        
    def draw(self, screen):
        currIntro = self.intros[self.currentIntroIdx]
        currIntroRect = currIntro.get_rect()
        currIntroRect.center = (320, 240)
        
        screen.blit(self.background, (0, 0))
        screen.blit(currIntro, currIntroRect)
        
class Intro(pygame.surface.Surface):
    def __init__(self, duration, text, image=None):
        pygame.surface.Surface.__init__(self, (320, 240))
        self.duration = duration
        self.content = pygame.surface.Surface((320, 240))
        
        # Include texts into content
        tmpContent = None
        idx = 0
        for i in text:
            tmpContent = data.render_text('genotype.ttf', 30, i, (255, 255, 255))
            self.content.blit(tmpContent, (0, idx))
            idx += 30
            
        self.blit(self.content, (0, 0))