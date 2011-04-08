'''The great director class.
'''

import pygame
import scene
import data

class Director(object):
    '''Manage the logic behind the scenes.
    '''

    defaults = {
        'size' : (640, 480),
        'title' : 'PyGame',
        'icon' : None,
        'icon_colorkey' : (255, 0, 255),
        'framerate' : 40,
        'show_fps' : False}

    def __init__(self, game, config=None):
        self.game = game

        self.config = {}
        self.config.update(self.defaults)

        if config:
            self.config.update(config)

        if self.config['icon']:
            icon = data.load_image(self.config['icon'])
            icon.set_colorkey(self.config['icon_colorkey'])
            pygame.display.set_icon(icon)

        if self.config['title']:
            pygame.display.set_caption(self.config['title'])

        self.screenMode = 0
        self.screen = pygame.display.set_mode(self.config['size'],self.screenMode)
        
        self.allSoundMute = False
        
        self.clock = pygame.time.Clock()
        self.running = True

        self.forceIndex = None
        self.index = None
        self.nextLoopScene = None
        self.nextLoopSceneReset = False
        self.scene = None
        self.scenes = []

    def register(self, name, klass, config=None):
        if not issubclass(klass, scene.Scene):
            raise TypeError('Class passed is not a Scene')
        self.scenes.append([name, klass, None, config])

    def change(self, name, reset=False):
        self.nextLoopScene = name
        self.nextLoopSceneReset = reset
        
    def doChange(self):
        name = self.nextLoopScene
        reset = self.nextLoopSceneReset
        if self.scene:
            self.scene.end()

        index = None

        for value in self.scenes:
            if value[0] == name:
                index = self.scenes.index(value)

        if index == None:
            raise KeyError('Scene %s not found' % (name, ))

        scene = self.scenes[index]

        if scene[2] == None or reset:
            klass = scene[1]

            if scene[3] == None:
                config = {}
            else:
                config = scene[3]

            scene[2] = klass(self.game, name, index, config)

        self.index = index
        self.scene = scene[2]
        self.scene.start()

    def changeAndBack(self, name):
        self.forceIndex = self.index
        self.change(name)

    def run(self):
        while self.running:
            self.clock.tick(self.config['framerate'])
            if not self.nextLoopScene == None:
                self.doChange()
                self.nextLoopScene = None
                self.nextLoopSceneReset = False
            
            if not self.scene:
                self.end()

            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    self.end()
                elif event.type == pygame.KEYDOWN and event.key == pygame.K_F11:
                    if self.screenMode != 0:
                        self.screenMode = 0
                    else:
                        self.screenMode = pygame.FULLSCREEN
                    self.screen = pygame.display.set_mode(self.config['size'],self.screenMode)
                else:
                    self.scene.handleEvent(event)

            #self.screen.fill((0, 0, 0))

            self.scene.update()
            self.scene.draw(self.screen)

            if self.config['show_fps']:
                font = data.load_font(data.FONT_MAIN, 23)
                fps = '%.1f' % self.clock.get_fps()
                text = font.render(fps, False, (255, 0, 255))

                rect = text.get_rect()
                rect.right = self.screen.get_width() - 5
                rect.bottom = self.screen.get_height() - 5

                self.screen.blit(text, rect)

            pygame.display.flip()

    def end(self):
        self.running = False

    def endScene(self, reset=False):
        if not self.forceIndex == None:
            self.change(self.scenes[self.forceIndex][0], reset)
            self.forceIndex = None
        elif self.index + 1 < len(self.scenes):
            self.change(self.scenes[self.index + 1][0], reset)
        else:
            self.end()
