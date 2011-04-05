'''The level classes.
'''

import pygame
import scene
import button
import data

class LevelScene(scene.Scene):
    '''Is the basic level.
    '''

    def __init__(self, game, count=9):
        super(LevelScene, self).__init__(game)

        self.sequence = button.SequenceButtonGroup((20, 20), (210, 100), 5, count)
        self.buttons = button.PlayableButtonGroup((50, 150), (35, 300), 15, count)

        self.count = count

        #self.sequence.play(1)
        self.running = False

        self.playing = True
        self.play = []

    def start(self, name):
        super(LevelScene, self).start(name)
        self.music_pre_bg = data.load_sound('pre-background.ogg', name)
        self.music_bg = data.load_sound('background.ogg', name)
        self.music_pre_bg.set_volume(0.1 )
        self.music_bg.set_volume(0.1 )
        self.music_pre_bg.play()
        self.music_bg.play(-1, fade_ms=4000)

        self.sequence.associateTheme(name) 
        self.buttons.associateTheme(name) 

    def end(self):
        self.music_bg.fadeout(2000)
        self.music_pre_bg.stop()
        super(LevelScene, self).end()

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
        screen.fill((255, 0, 255))

        self.sequence.draw(screen)
        self.buttons.draw(screen)
