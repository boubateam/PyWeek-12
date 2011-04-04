'''The level classes.
'''

import pygame
import scene
import button

class LevelScene(scene.Scene):
    '''Is the basic level.
    '''

    def __init__(self, game, count=9):
        super(LevelScene, self).__init__(game)

        self.sequence = button.SequenceButtonGroup((20, 20), (210, 100), 5)
        self.buttons = button.PlayableButtonGroup((50, 150), (35, 300), 15)

        #self.sequence.play(1)

    def handleEvent(self, event):
        if event.type == pygame.KEYDOWN:
            if event.key == pygame.K_ESCAPE:
                self.game.director.changeAndBack('pause')
        elif event.type == pygame.MOUSEBUTTONUP:
            self.buttons.click(event)

    def update(self):
        self.sequence.update()
        self.buttons.update()

    def draw(self, screen):
        self.sequence.draw(screen)
        self.buttons.draw(screen)
