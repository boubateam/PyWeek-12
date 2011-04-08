'''The credits scene.
'''

import pygame
import scene
import data

class HowtoScene(scene.Scene):
    def __init__(self, game, name, index, config=None):
        super(HowtoScene, self).__init__(game, name, index, config)

        self.text = data.render_text(data.FONT_MAIN, 37, 'Push the button !', (255, 255, 255))
        self.textrect = self.text.get_rect()

        self.background = data.load_image('credits.png')
        self.music_bg = data.load_sound('credits.ogg')

    def start(self):
        self.music_bg.play(-1, fade_ms=1000)

    def end(self):
        self.music_bg.fadeout(1000)

    def handleEvent(self, event):
        if event.type == pygame.KEYDOWN:
            if event.key == pygame.K_ESCAPE:
                self.game.director.endScene()

    def update(self):
        x = 320
        y = 60

        self.textrect.center = (x, y)
        y += self.textrect.height * 1.5

    def draw(self, screen):
        screen.blit(self.background, (0, 0))
        screen.blit(self.text, self.textrect)
