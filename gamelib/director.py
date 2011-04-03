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

    def __init__(self, config=None):
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

        self.screen = pygame.display.set_mode(self.config['size'])
        self.clock = pygame.time.Clock()
        self.running = True

        self.scene = None
        self.scenes = {}

    def register(self, name, klass):
        if name in self.scenes:
            raise KeyError('Scene %s already registered' % (name, ))
        if not issubclass(klass, scene.Scene):
            raise TypeError('Class passed is not a Scene')

        self.scenes[name] = klass(self)

    def unregister(self, name):
        if not name in self.scenes:
            raise KeyError('Scene %s not found' % (name, ))

        del self.scenes[name]

    def change(self, name):
        if not name in self.scenes:
            raise KeyError('Scene %s not found' % (name, ))

        if self.scene:
            self.scene.end()

        self.scene = self.scenes[name]
        self.scene.start()

    def run(self):
        while self.running:
            self.clock.tick(self.config['framerate'])

            if not self.scene:
                self.end()

            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    self.end()
                else:
                    self.scene.handleEvent(event)

            self.screen.fill((0, 0, 0))

            self.scene.update()
            self.scene.draw(self.screen)

            if self.config['show_fps']:
                font = pygame.font.Font(None, 23)
                fps = '%.1f' % self.clock.get_fps()
                text = font.render(fps, False, (255, 0, 255))

                rect = text.get_rect()
                rect.right = self.screen.get_width() - 5
                rect.bottom = self.screen.get_height() - 5

                self.screen.blit(text, rect)

            pygame.display.flip()

    def end(self):
        self.running = False
