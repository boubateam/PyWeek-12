'''The level class.
'''

import pygame
import scene
import button

class Level(scene.Scene):
    '''Is the basic level.
    '''
    def __init__(self, game):
        super(Level, self).__init__(game)

        self.text = self._create(37, 'Hello World from level')
        self.textrect = self.text.get_rect()
        self.buttonList = button.ButtonsList(game)
        self.buttonList.debug()

    def _create(self, fontsize, text):
        font = pygame.font.Font(None, fontsize)
        rend = font.render(text, False, (255, 255, 255))

        return rend

    def start(self):
        pass
    
    def end(self):
        pass
    
    def handleEvent(self, event):
        
        if event.type == pygame.KEYDOWN:
            if event.key == pygame.K_SPACE:
                self.game.director.changeAndBack('pause')

    def update(self):
        self.textrect.center = (320, 240)

    def draw(self, screen):
        screen.blit(self.text, self.textrect)
        rectbase = self.text.get_rect()
        rectbase[1] += 50
        for i in self.buttonList.buttons:
            rectbase[0] += 50
            screen.blit(i.image, rectbase)