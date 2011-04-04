'''The game over scene.
'''

import pygame
import scene
import data

class GameOverScene(scene.Scene):
    def __init__(self, game):
        super(GameOverScene, self).__init__(game)

        self.text = data.render_text(None, 37, 'Game Over', (255, 255, 255))
        self.textrect = self.text.get_rect()

    def handleEvent(self, event):
        if event.type == pygame.KEYDOWN or event.type == pygame.MOUSEBUTTONUP:
            self.game.end()

    def update(self):
        self.textrect.center = (320, 240)

    def draw(self, screen):
        screen.blit(self.text, self.textrect)
