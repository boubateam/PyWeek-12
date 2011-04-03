'''The intro scene.
'''

import time
import pygame
import scene

class Pause(scene.Scene):
    def __init__(self, game):
        super(Pause, self).__init__(game)

        self.text = self._create(37, 'Pause')
        self.textrect = self.text.get_rect()

    def _create(self, fontsize, text):
        font = pygame.font.Font(None, fontsize)
        rend = font.render(text, False, (255, 255, 255))

        return rend

    def handleEvent(self, event):
        if event.type == pygame.KEYDOWN:
            if event.key == pygame.K_SPACE:
                self.game.director.endScene()

    def update(self):
        self.textrect.center = (320, 240)

    def draw(self, screen):
        screen.blit(self.text, self.textrect)
