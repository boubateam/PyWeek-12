'''The level class.
'''

import pygame
import scene

class Level(scene.Scene):
    '''Is the basic level.
    '''
    def __init__(self, director):
        super(Level, self).__init__(director)

        self.text = self._create(37, 'Hello World from level')
        self.textrect = self.text.get_rect()

    def _create(self, fontsize, text):
        font = pygame.font.Font(None, fontsize)
        rend = font.render(text, False, (255, 255, 255))

        return rend

    def start(self):
        pass
    
    def end(self):
        pass
    
    def handleEvent(self, event):
        pass

    def update(self):
        self.textrect.center = (320, 240)

    def draw(self, screen):
        screen.blit(self.text, self.textrect)