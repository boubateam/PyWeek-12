'''The intro scene.

04/04/2011 : add sound
'''

import pygame
import scene
import data

class IntroScene(scene.Scene):
    def __init__(self, game):
        super(IntroScene, self).__init__(game)

        self.text = data.render_text('LiberationSans-Regular.ttf', 37, 'Welcome to Garfunkel', (255, 255, 255))
        self.textrect = self.text.get_rect()
        self.music = data.load_sound('intro.ogg')

    def start(self):
        super(IntroScene, self).start()
        self.music.play(-1)

    def end(self):
        self.music.stop()
        super(IntroScene, self).end()

    def handleEvent(self, event):
        if event.type == pygame.KEYDOWN:
            if event.key == pygame.K_ESCAPE:
                self.game.end()
            elif event.key == pygame.K_SPACE:
                self.game.director.endScene()

    def update(self):
        self.textrect.center = (320, 240)

    def draw(self, screen):
        screen.blit(self.text, self.textrect)
