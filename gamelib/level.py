'''The level classes.
'''

import pygame
import scene
import button
import data
import string

class LevelScene(scene.Scene):
    '''Is the basic level.
    '''

    def __init__(self, game, name, index, config=None):
        super(LevelScene, self).__init__(game, name, index, config)

        self.font = data.load_font(data.FONT_FIX, 23)

        self.count = config['count'] if 'count' in config else 9
        self.delta = config['delta'] if 'delta' in config else 1000

        self.points = config['points'] if 'points' in config else 500
        self.volume = config['volume'] if 'volume' in config else 0.3
        self.pointsMulti = config['pointsMulti'] if 'pointsMulti' in config else 1
        self.pointsText = None

        self.sequence = button.SequenceButtonGroup((20, 20), (210, 100), 15, 5, self.count, self.delta)
        self.buttons = button.PlayableButtonGroup((50, 150), (35, 300), 20, 15, self.count, 750)

        self.seqindex = 0
        self.sequencing = False

        self.play = []
        self.playing = False

        self.background = data.load_image('background.png')
        self.ray = data.load_image('ray.png')
        self.piano = data.load_image('piano.png')

        self.music_bg = data.load_sound('background.ogg', self.name)
        self.music_bg.set_volume(self.volume)
        self.music_pre_bg = data.load_sound('pre-background.ogg', self.name)
        self.music_pre_bg.set_volume(0.3)

        self.sequence.associateTheme(self.name) 
        self.buttons.associateTheme(self.name)

        self.pre_bg_channel = None
        self.bg_channel = None

        # step counter management
        self.stepElapsingInTime = 1
        self.stepElapsedTimeCounter = 0
        self.counterStepPerClick = config['timetoclick'] if 'timetoclick' in config else 200
        self.currentCounterStep = self.counterStepPerClick

        # counting only when button animation is over
        self.stepCountElapsingTime = False
        self.stepCounterText = None
        self.rectWidth = 0

        boss = data.load_image('boss.png', self.name)
        boss.set_colorkey((255, 0, 255))
        
        miniboss = data.load_image('boss_mini.png', self.name)
        miniboss.set_colorkey((255, 0, 255))    
            
        self.animMiniBossImage = miniboss # pygame.transform.scale(boss, (170, 170))
        self.animMiniBossRect = self.animMiniBossImage.get_rect()
        self.animMiniBossRect.left = 302
        self.animMiniBossRect.bottom = 243
        
        self.animBossAction = 'scale'
        self.animBossActionCount = 0
        self.animBossImage = boss # pygame.transform.scale(boss, (170, 170))
        self.animBossRect = self.animBossImage.get_rect()
        self.animBossRect.left = 350
        self.animBossRect.bottom = 280
        self.animBossTime = 0
        self.animBossShowRaw = False

        self.counterRect = [266,250,110,8]
        self.counterRectDecSizePerStep = 110.0/self.counterStepPerClick

        self.incrRedColorUnit = 255.0/self.counterStepPerClick
        self.decrBlueColorUnit = 255.0/self.counterStepPerClick

        self.bottomPanel = pygame.Surface((640,240))
        self.bottomPanel.fill((100, 100, 100))
        self.bottomPanel.set_alpha(200)

        self.bottomText     = data.render_text(data.FONT_MAIN, 30, self.name.replace('-', ' ') + " starting in...", (255, 0, 0))
        self.bottomTextRect = self.bottomText.get_rect()
        self.bottomTextRect.center = (320, 360)

        #self.seqStart()

    def start(self):
        if self.bg_channel == None:
            self.bg_channel =  self.music_bg.play(-1, fade_ms=100)
        else:
            self.bg_channel.unpause()

        if self.pre_bg_channel == None:
            self.pre_bg_channel =  self.music_pre_bg.play(fade_ms=100)
        else:
            self.pre_bg_channel.unpause()

        if not self.playing and not self.sequencing:
            self.animBossTime = pygame.time.get_ticks() + 150

    def end(self):
        if self.bg_channel != None :
            self.bg_channel.pause()
        if self.pre_bg_channel != None :
            self.pre_bg_channel.pause()

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
                lessPoints = self.currentCounterStep
                sumPoints = False

                self.play.append(index)
                self.currentCounterStep = self.counterStepPerClick

                if not self.sequence.validate(self.play):
                    self.game.director.change('gameover')
                elif len(self.play) == self.count:
                    self.game.director.endScene(True)
                elif len(self.play) == self.seqindex:
                    sumPoints = True

                    self.playing = False
                    self.seqStart()
                else:
                    sumPoints = True

                if sumPoints:
                    self.game.points += (self.points - (self.counterStepPerClick - lessPoints)) * self.pointsMulti

    def oneButtonALaFois(self):
        
        for i in self.buttons:
            if i.active :
                return True
            
        return False
        
    def update(self):
        self.sequence.update()
        self.buttons.update()
        self.pointsText = self.font.render('%d' % (self.game.points, ), False, (255, 255, 255))

        if self.stepCountElapsingTime and not self.oneButtonALaFois():
            if pygame.time.get_ticks() > self.stepElapsedTimeCounter:
                self.currentCounterStep -= 1
                self.stepElapsedTimeCounter = pygame.time.get_ticks() + self.stepElapsingInTime
            if self.currentCounterStep < 0:
                self.game.director.change('gameover')

        if not self.playing and not self.sequencing:
            if pygame.time.get_ticks() > self.animBossTime:
                self.animBossTime += 150

                if self.animBossAction == 'scale':
                    self.animBossActionCount += 1

                    self.animBossImage = pygame.transform.scale(self.animBossImage,
                        (self.animBossRect.w - 9, self.animBossRect.h - 9))

                    bottom = self.animBossRect.bottom
                    left = self.animBossRect.left

                    self.animBossRect = self.animBossImage.get_rect()
                    self.animBossRect.bottom = bottom - 2
                    self.animBossRect.left = left - 4

                    if self.animBossActionCount == 15:
                        self.animBossActionCount = 0
                        self.animBossAction = 'moveup'
                        self.animBossShowRaw = True

                    self.bottomTextRect.center = (320, 360)

                elif self.animBossAction == 'moveup':
                    
                    self.animBossRect = self.animMiniBossImage.get_rect()
                    self.bottomText = data.render_text(data.FONT_MAIN, 30, str(4 - (self.animBossActionCount / 4)), (255, 0, 0))
                    self.bottomTextRect = self.bottomText.get_rect()
                    self.bottomTextRect.center = (320, 360)

                    self.animBossActionCount += 1

                    if self.animBossActionCount <= 10:
                        self.animMiniBossRect.top -= 5
                    elif self.animBossActionCount > 10 and self.animBossActionCount < 20:
                        rect = pygame.Rect(0, 5,
                                           self.animMiniBossRect.w,
                                           self.animMiniBossRect.h - 5,
                                           )
                        self.animMiniBossImage = self.animMiniBossImage.subsurface(rect)
                        self.animMiniBossRect.h -= 5
                    elif self.animBossActionCount == 20:
                        self.animBossActionCount = 0
                        self.animBossAction = None
                        self.animBossShowRaw = False
                        self.background = data.load_image('background.png', self.name)
                else:
                    self.seqStart()

    def draw(self, screen):
        screen.blit(self.background, (0, 0))

        if self.animBossShowRaw:
            screen.blit(self.ray, (260, 158))

        widthF = int(self.counterRectDecSizePerStep * self.currentCounterStep)
        redColo = int(self.incrRedColorUnit * self.currentCounterStep)
        blueColo = int(self.decrBlueColorUnit * self.currentCounterStep)
        self.incrRedColorUnit = 255.0 / self.counterStepPerClick
        self.decrBlueColorUnit = 255.0 / self.counterStepPerClick
        tmpv = 255-redColo

        if tmpv > 255:
            redColo = 255
        if blueColo < 0:
            blueColo = 0

        pygame.draw.rect(screen, (255-redColo,0,blueColo), (self.counterRect[0], self.counterRect[1], widthF, self.counterRect[3]))     

        self.sequence.draw(screen)
        self.buttons.draw(screen)

        screen.blit(self.pointsText, (10, 10))

        if not self.playing and not self.sequencing:
            if self.animBossAction=='moveup':
                screen.blit(self.animMiniBossImage, self.animMiniBossRect)
            else:
                screen.blit(self.animBossImage, self.animBossRect)
                
            screen.blit(self.piano, (0,240))
            screen.blit(self.bottomPanel, (0, 240))
            screen.blit(self.bottomText, self.bottomTextRect)
