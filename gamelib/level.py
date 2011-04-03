'''The level class.
'''

import pygame
import scene

class Level(scene.Scene):
    '''Is the basic level.
    '''

    def __init__(self, game):
        super(Level, self).__init__(game)

        self.text = self._create(37, 'Hello World from Level')
        self.textrect = self.text.get_rect()

    def _create(self, fontsize, text):
        font = pygame.font.Font(None, fontsize)
        rend = font.render(text, False, (255, 255, 255))

        return rend

    def handleEvent(self, event):
        if event.type == pygame.KEYDOWN:
            if event.key == pygame.K_ESCAPE:
                self.game.director.changeAndBack('pause')

    def update(self):
        self.textrect.center = (320, 240)

    def draw(self, screen):
        screen.blit(self.text, self.textrect)
