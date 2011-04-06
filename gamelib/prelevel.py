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

        self.text     = data.render_text('acmesa.ttf', 30, 'Get ready...', (255, 0, 0))
        self.textrect = self.text.get_rect()
        self.ttl      = 5
        
        self.music_pre_bg = data.load_sound('pre-background.ogg')
        

    def start(self):
        self.music_pre_bg.play(-1, fade_ms=200)

    def end(self):
        self.music_pre_bg.fadeout(100)

    def handleEvent(self, event):
        pass 

    def update(self):
        
        if self.ttl < 4 :
            self.textrect.center = (400, 240)
            self.text = data.render_text('acmesa.ttf', 30, str(self.ttl), (255, 0, 0))
        else :
            self.textrect.center = (320, 240)
        
        

    def draw(self, screen):
        screen.fill((200, 200, 200))
        screen.blit(self.text, self.textrect)
        pygame.time.wait(600)
        self.ttl -= 1
        if self.ttl < 0:
            self.game.director.endScene()
