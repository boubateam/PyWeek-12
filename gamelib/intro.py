'''The intro scene.
'''

import time
import pygame
import scene
import data

class IntroScene(scene.Scene):
    def __init__(self, game):
        super(IntroScene, self).__init__(game)

        self.text = self._create(37, 'Hello World')
        self.textrect = self.text.get_rect()
        self.music = pygame.mixer.Sound(data.filepath('intro.ogg'))
         
        
    def start(self):
        super(IntroScene, self).start()
        self.music.play(-1) 
        print('intro.start()')   
    
    def end(self):
        
        self.music.stop() 
        print('inro.end()') 
        super(IntroScene, self).end()
    
        
    def _create(self, fontsize, text):
        font = pygame.font.Font(None, fontsize)
        rend = font.render(text, False, (255, 255, 255))

        return rend

    def handleEvent(self, event):
        if event.type == pygame.KEYDOWN:
            if event.key == pygame.K_ESCAPE:
                self.game.end()
            elif event.key == pygame.K_SPACE:
                self.game.director.endScene()

    def update(self):
        self.textrect.center = (320, 240)

    def draw(self, screen):
        screen.blit(self.text, self.textrect)
        
