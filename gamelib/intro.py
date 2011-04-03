'''The intro scene.
'''

import pygame
import scene

class IntroScene(scene.Scene):
    def __init__(self, director):
        super(IntroScene, self).__init__(director)

        self.text = self._create(37, 'Hello World')
        self.textrect = self.text.get_rect()

    def _create(self, fontsize, text):
        font = pygame.font.Font(None, fontsize)
        rend = font.render(text, False, (255, 255, 255))

        return rend

    def changed(self):
        pass

    def event(self, event):
        if event.type == pygame.KEYDOWN:
            if event.key == pygame.K_ESCAPE:
                self.director.end()

    def update(self):
        self.textrect.center = (320, 240)

    def draw(self, screen):
        screen.blit(self.text, self.textrect)
