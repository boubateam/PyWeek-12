'''The credits scene.
'''

import pygame
import scene
import data

class CreditsScene(scene.Scene):
    def __init__(self, game, name, index, config=None):
        super(CreditsScene, self).__init__(game, name, index, config)

        self.text = data.render_text('ace.ttf', 37, 'Thanks for Playing', (255, 255, 255))
        self.textrect = self.text.get_rect()

        font = data.load_font('LiberationSans-Regular.ttf', 17)
        names = ('ahsio', 'cyqui', 'gleuh', 'greg0ire', 'joksnet')

        self.designLabel = data.render_text('acmesa.ttf', 23, 'Design:', (255, 255, 127))
        self.designLabelRect = self.designLabel.get_rect()
        self.design = data.render_text('LiberationSans-Regular.ttf', 21, 'tocab', (255, 255, 255))
        self.designRect = self.design.get_rect()

        self.musicLabel = data.render_text('acmesa.ttf', 23, 'Music:', (255, 255, 127))
        self.musicLabelRect = self.musicLabel.get_rect()
        self.music = data.render_text('LiberationSans-Regular.ttf', 21, 'TOTOleHero', (255, 255, 255))
        self.musicRect = self.music.get_rect()

        self.names = []

        for name in names:
            rend = font.render(name, True, (255, 255, 255))
            rect = rend.get_rect()

            self.names.append((rend, rect))

        self.team = data.render_text('genotype.ttf', 37, 'The Bouba Team', (60, 255, 60))
        self.teamRect = self.team.get_rect()

        self.background = data.load_image('credits.png')
        self.music_bg = data.load_sound('credits.ogg')

    def start(self):
        self.music_bg.play(-1, fade_ms=1000)

    def end(self):
        self.music_bg.fadeout(1000)

    def handleEvent(self, event):
        if event.type == pygame.KEYDOWN:
            if event.key == pygame.K_ESCAPE:
                self.game.director.endScene()

    def update(self):
        x = 320
        y = 60

        self.textrect.center = (x, y)
        y += self.textrect.height * 2

        self.designLabelRect.topleft = (25, y)
        self.designRect.topleft = (self.designLabelRect.right + 7, y + 6)

        self.musicRect.topright = (640 - 25, y + 6)
        self.musicLabelRect.topright = (self.musicRect.left - 7, y)

        y += self.musicLabelRect.height * 2

        for value in self.names:
            value[1].center = (x, y)
            y += value[1].height * 1.5

        y += 35
        self.teamRect.topright = (640 - 25, y)

    def draw(self, screen):
        #screen.blit(self.background, (0, 0))
        screen.fill((0, 0, 0))

        screen.blit(self.text, self.textrect)
        screen.blit(self.design, self.designRect)
        screen.blit(self.designLabel, self.designLabelRect)
        screen.blit(self.music, self.musicRect)
        screen.blit(self.musicLabel, self.musicLabelRect)

        for rend, rect in self.names:
            screen.blit(rend, rect)

        screen.blit(self.team, self.teamRect)
