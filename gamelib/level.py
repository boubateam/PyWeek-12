'''The level classes.
'''

import pygame
import scene
import button
import data

class LevelScene(scene.Scene):
    '''Is the basic level.
    '''

    def __init__(self, game, name, index, config=None):
        super(LevelScene, self).__init__(game, name, index, config)

        if config and 'count' in config:
            self.count = config['count']
        else:
            self.count = 9

        self.sequence = button.SequenceButtonGroup((20, 20), (210, 100), 5, self.count)
        self.buttons = button.PlayableButtonGroup((50, 150), (35, 300), 15, self.count)

        self.seqindex = 0
        self.sequencing = False

        self.play = []
        self.playing = False

        self.music_pre_bg = data.load_sound('pre-background.ogg', self.name)
        self.music_bg = data.load_sound('background.ogg', self.name)
        self.music_pre_bg.set_volume(0.3)
        self.music_bg.set_volume(0.3)

        self.sequence.associateTheme(self.name) 
        self.buttons.associateTheme(self.name)
        
        self.pre_bg_channel = None
        self.bg_channel = None
        
        self.seqStart()

    def start(self):
        if self.pre_bg_channel == None :
            self.pre_bg_channel = self.music_pre_bg.play()
        else:
            self.pre_bg_channel.unpause()
        
        if self.bg_channel == None :
            self.bg_channel =  self.music_bg.play(-1, fade_ms=4000)
        else:
            self.bg_channel.unpause()

    def end(self):

        if self.pre_bg_channel != None :
            self.pre_bg_channel.pause()
        if self.bg_channel != None :
            self.bg_channel.pause()    

    def seqStart(self):
        self.seqindex += 1
        self.sequence.play(self.seqindex, self.seqEnd)
        self.sequencing = True

    def seqEnd(self):
        self.sequencing = False
        self.playing = True
        self.play = []

    def handleEvent(self, event):
        index = None
        
        if event.type == pygame.KEYDOWN:
            if event.key == pygame.K_ESCAPE:
                self.game.director.changeAndBack('pause')
            elif event.key in range(pygame.K_1,pygame.K_9 ):
                index = event.key - pygame.K_1  
                index = self.buttons.push(index)
                
        elif self.playing and event.type == pygame.MOUSEBUTTONUP:
            index = self.buttons.click(event.pos)

        if index != None:

            self.play.append(index)

            if not self.sequence.validate(self.play):
                self.game.director.change('gameover')
            elif len(self.play) > self.count:
                self.game.director.endScene()
            elif len(self.play) == self.seqindex:
                self.playing = False
                self.seqStart()

    def update(self):
        self.sequence.update()
        self.buttons.update()

    def draw(self, screen):
        screen.fill((255, 255, 255))

        self.sequence.draw(screen)
        self.buttons.draw(screen)
