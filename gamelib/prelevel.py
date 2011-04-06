'''Scene played before a level to get the player ready
'''

import pygame
import scene
import data

class PreLevelScene(scene.Scene):
    '''Represents an abstract scene.
    '''

    name = ''

    def __init__(self, game, name, index, config=None):
        super(PreLevelScene, self).__init__(game, name, index, config)

        self.text     = data.render_text('genotype.ttf', 30, 'Get ready', (255, 0, 0))
        self.textrect = self.text.get_rect()
        self.ttl      = 10

    def start(self):
        pass

    def end(self):
        pass

    def handleEvent(self, event):
        pass 

    def update(self):
        self.textrect.center = (320, 240)

    def draw(self, screen):
        screen.fill((200, 200, 200))
        screen.blit(self.text, self.textrect)
        pygame.time.wait(300)
        self.ttl -= 1
        if (self.ttl < 0):
            self.game.director.endScene()
