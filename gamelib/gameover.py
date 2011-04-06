'''The game over scene.
'''

import pygame
import scene
import data

class GameOverScene(scene.Scene):
    def __init__(self, game, name, index, config=None):
        super(GameOverScene, self).__init__(game, name, index, config)

        self.text = data.render_text('genotype.ttf', 37, 'Game Over', (255, 255, 255))
        self.textrect = self.text.get_rect()
        self.background = data.load_image('gameover.png')

        self.music_bg = data.load_sound('gameover.ogg')
    
    def start(self):
        self.music_bg.play()
        
    def handleEvent(self, event):
        if event.type == pygame.KEYDOWN or event.type == pygame.MOUSEBUTTONUP:
            self.game.director.change('topscore')

    def update(self):
        self.textrect.center = (320, 240)

    def draw(self, screen):
        screen.blit(self.background, (0, 0))
        screen.blit(self.text, self.textrect)
