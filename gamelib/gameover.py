'''The game over scene.
'''

import pygame
import scene

class GameOverScene(scene.Scene):
    def __init__(self, game):
        super(GameOverScene, self).__init__(game)

        self.text = self._create(37, 'Game Over')
        self.textrect = self.text.get_rect()

    def _create(self, fontsize, text):
        font = pygame.font.Font(None, fontsize)
        rend = font.render(text, False, (255, 255, 255))

        return rend

    def handleEvent(self, event):
        if event.type == pygame.KEYDOWN or event.type == pygame.MOUSEBUTTONUP:
            self.game.end()

    def update(self):
        self.textrect.center = (320, 240)

    def draw(self, screen):
        screen.blit(self.text, self.textrect)
