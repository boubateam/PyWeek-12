'''The game over scene.
'''

import pygame
import scene
import data

class TopScoreScene(scene.Scene):
    def __init__(self, game, name, index, config=None):
        super(TopScoreScene, self).__init__(game, name, index, config)

        self.text = data.render_text('LiberationSans-Regular.ttf', 17, 'Who\'s the rockstar with 1000 points ?', (255, 255, 255))
        self.textrect = self.text.get_rect()
        self.music_bg = data.load_sound('intro.ogg')
        self.background = data.load_image('intro.png')
        
    def start(self):
        self.music_bg.play()
        
    def handleEvent(self, event):
        '''if event.type == pygame.KEYDOWN:
            self.game.director.change('menu')
            '''

    def update(self):
        self.textrect.center = (320, 20)

    def draw(self, screen):
        screen.blit(self.background, (0, 0))
        screen.blit(self.text, self.textrect)
