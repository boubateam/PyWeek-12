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

        self.font = data.load_font(None, 23)

        self.count = config['count'] if 'count' in config else 9
        self.delta = config['delta'] if 'delta' in config else 1000

        self.points = config['points'] if 'points' in config else 100
        self.pointsMulti = config['pointsMulti'] if 'pointsMulti' in config else 1
        self.pointsText = None

        self.sequence = button.SequenceButtonGroup((20, 20), (210, 100), 15, 5, self.count, self.delta)
        self.buttons = button.PlayableButtonGroup((50, 150), (35, 300), 20, 15, self.count, self.delta)

        self.seqindex = 0
        self.sequencing = False

        self.play = []
        self.playing = False

        self.background = data.load_image('background.png')

        self.music_bg = data.load_sound('background.ogg', self.name)
        self.music_bg.set_volume(0.3)

        self.sequence.associateTheme(self.name) 
        self.buttons.associateTheme(self.name)

        self.pre_bg_channel = None
        self.bg_channel = None

        # step counter management
        self.stepElapsingInTime = 1
        self.stepElapsedTimeCounter = 0
        self.counterStepPerClick = 500
        self.currentCounterStep = self.counterStepPerClick

        # counting only when button animation is over
        self.stepCountElapsingTime = False
        self.stepCounterText = None

        boss = data.load_image('boss.png', self.name)
        boss.set_colorkey((255, 0, 255))

        self.animBossAction = 'scale'
        self.animBossActionCount = 0
        self.animBossImage = pygame.transform.scale(boss, (170, 170))
        self.animBossRect = self.animBossImage.get_rect()
        self.animBossRect.left = 360
        self.animBossRect.bottom = 240
        self.animBossTime = pygame.time.get_ticks() + 350

        #self.seqStart()

    def start(self):
        if self.bg_channel == None :
            self.bg_channel =  self.music_bg.play(-1, fade_ms=100)
        else:
            self.bg_channel.unpause()

    def end(self):
        if self.bg_channel != None :
            self.bg_channel.pause()

    def seqStart(self):
        self.seqindex += 1
        self.sequence.play(self.seqindex, self.seqEnd)
        self.sequencing = True
        self.stepCountElapsingTime = False

    def seqEnd(self):
        self.sequencing = False
        self.playing = True
        self.play = []
        self.stepCountElapsingTime = True

    def handleEvent(self, event):
        index = None

        if event.type == pygame.KEYDOWN:
            if event.key == pygame.K_ESCAPE:
                self.game.director.changeAndBack('pause')
            elif event.key in range(pygame.K_1, pygame.K_9):
                index = event.key - pygame.K_1
                index = self.buttons.push(index)

        elif self.playing and event.type == pygame.MOUSEBUTTONUP:
            index = self.buttons.click(event.pos)

            if index != None:
                self.play.append(index)
                self.currentCounterStep = self.counterStepPerClick

                if not self.sequence.validate(self.play):
                    self.game.director.change('gameover')
                elif len(self.play) == self.count:
                    self.game.director.endScene(True)
                elif len(self.play) == self.seqindex:
                    self.game.points += self.points * self.pointsMulti
                    self.playing = False
                    self.seqStart()

    def update(self):
        self.sequence.update()
        self.buttons.update()

        self.pointsText = self.font.render('%d' % (self.game.points, ), False, (255, 255, 255))

        if self.stepCountElapsingTime:
            if pygame.time.get_ticks() > self.stepElapsedTimeCounter:
                self.currentCounterStep -=1
                self.stepElapsedTimeCounter = pygame.time.get_ticks()+self.stepElapsingInTime

            if self.currentCounterStep < 0:
                self.game.director.change('gameover')
        
        if not self.playing and not self.sequencing:
            if pygame.time.get_ticks() > self.animBossTime:
                self.animBossTime += 350

                if self.animBossAction == 'scale':
                    self.animBossActionCount += 1

                    self.animBossImage = pygame.transform.scale(self.animBossImage,
                        (self.animBossRect.w - 10, self.animBossRect.h - 10))

                    bottom = self.animBossRect.bottom
                    left = self.animBossRect.left

                    self.animBossRect = self.animBossImage.get_rect()
                    self.animBossRect.bottom = bottom
                    self.animBossRect.left = left - 5

                    if self.animBossActionCount == 13:
                        self.animBossActionCount = 0
                        self.animBossAction = 'moveup'
                elif self.animBossAction == 'moveup':
                    self.animBossActionCount += 1
                    self.animBossRect.top -= 5

                    if self.animBossActionCount == 16:
                        self.animBossActionCount = 0
                        self.animBossAction = None
                else:
                    self.seqStart()

    def draw(self, screen):
        self.stepCounterText = data.render_text('LiberationSans-Regular.ttf', 15, "time "+str(self.currentCounterStep), (255, 0,0))

        screen.blit(self.background, (0, 0))
        screen.blit(self.stepCounterText, (300,0))

        self.sequence.draw(screen)
        self.buttons.draw(screen)

        screen.blit(self.pointsText, (10, 10))

        if not self.playing and not self.sequencing:
            screen.blit(self.animBossImage, self.animBossRect)
