'''The credits scene.
'''

import pygame
import scene

class CreditsScene(scene.Scene):
    def __init__(self, game):
        super(CreditsScene, self).__init__(game)

        self.text = self._create(37, 'Bouba Team')
        self.textrect = self.text.get_rect()

        names = ('ahsio', 'cyqui', 'gleuh', 'greg0ire', 'joksnet',
            'tocab', 'TOTOleHero')

        self.names = []

        for name in names:
            rend = self._create(17, name)
            rect = rend.get_rect()

            self.names.append((rend, rect))

    def _create(self, fontsize, text):
        font = pygame.font.Font(None, fontsize)
        rend = font.render(text, False, (255, 255, 255))

        return rend

    def handleEvent(self, event):
        if event.type == pygame.KEYDOWN:
            if event.key == pygame.K_ESCAPE:
                self.game.director.endScene()

    def update(self):
        x = 320
        y = 60

        self.textrect.center = (x, y)
        y += self.textrect.height * 1.5

        for value in self.names:
            value[1].center = (x, y)
            y += value[1].height * 1.5

    def draw(self, screen):
        screen.blit(self.text, self.textrect)

        for rend, rect in self.names:
            screen.blit(rend, rect)
