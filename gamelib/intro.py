'''The intro scene.

04/04/2011 : add sound
'''

import pygame
import scene
import data

class IntroScene(scene.Scene):
    def __init__(self, game, name, index, config=None):
        super(IntroScene, self).__init__(game, name, index, config)

        self.text = data.render_text('LiberationSans-Regular.ttf', 37, 'Welcome to Garfunkel', (255, 255, 255))
        self.textrect = self.text.get_rect()

        self.background = data.load_image('intro.png')
        self.music = data.load_sound('intro.ogg')

    def start(self):
        self.music.play(-1,fade_ms=4000)

    def end(self):
        self.music.fadeout(2000)

    def handleEvent(self, event):
        if event.type == pygame.KEYDOWN:
            if event.key == pygame.K_ESCAPE:
                self.game.end()
            elif event.key == pygame.K_SPACE:
                self.game.director.endScene()

    def update(self):
        self.textrect.center = (320, 240)

    def draw(self, screen):
        screen.blit(self.background, (0, 0))
        screen.blit(self.text, self.textrect)
