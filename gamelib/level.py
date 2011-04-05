'''The level classes.
'''

import pygame
import scene
import button
import data

class LevelScene(scene.Scene):
    '''Is the basic level.
    '''

    def __init__(self, game, name, index):
        super(LevelScene, self).__init__(game, name, index)

        self.count = 9

        self.sequence = button.SequenceButtonGroup((20, 20), (210, 100), 5, self.count)
        self.buttons = button.PlayableButtonGroup((50, 150), (35, 300), 15, self.count)

        #self.sequence.play(1)
        self.running = False

        self.playing = True
        self.play = []

        self.music_pre_bg = data.load_sound('pre-background.ogg', self.name)
        self.music_bg = data.load_sound('background.ogg', self.name)
        self.music_pre_bg.set_volume(0.5)
        self.music_bg.set_volume(0.5)

        self.sequence.associateTheme(self.name) 
        self.buttons.associateTheme(self.name)

    def start(self):
        self.music_pre_bg.play()
        self.music_bg.play(-1, fade_ms=4000) 

    def end(self):
        self.music_bg.fadeout(2000)
        self.music_pre_bg.stop()

    def handleEvent(self, event):
        if event.type == pygame.KEYDOWN:
            if event.key == pygame.K_ESCAPE:
                self.game.director.changeAndBack('pause')
        elif self.playing and event.type == pygame.MOUSEBUTTONUP:
            index = self.buttons.click(event.pos)

            if index:
                self.play.append(index)

                if not self.sequence.validate(self.play):
                    self.game.director.change('gameover')
                elif len(self.play) > self.count:
                    self.game.director.endScene()

    def update(self):
        self.sequence.update()
        self.buttons.update()

    def draw(self, screen):
        screen.fill((255, 255, 255))

        self.sequence.draw(screen)
        self.buttons.draw(screen)
