'''The credits scene.
'''

import pygame
import scene
import data

class HowtoScene(scene.Scene):
    def __init__(self, game, name, index, config=None):
        super(HowtoScene, self).__init__(game, name, index, config)

        self.bg_text = data.load_image('howtoplay.png')
        self.bg_text = pygame.transform.scale(self.bg_text, (534, 400))
        self.bg_textrect = self.bg_text.get_rect()
        
        fontText = data.load_font(data.FONT_MAIN, 20)
        fontText.set_bold(True)
        
        texts = [
            {'text':'1) The boss generates 1 to 9 sounds', 'top':30, 'left':50},
            {'text':'2) You must copy the generated sequence', 'top':250, 'left':20}
        ]
        
        for phrase in texts:
            text = fontText.render(phrase['text'], True, (255, 255, 255))
            textrect = text.get_rect()
            textrect.top = phrase['top']
            textrect.left = phrase['left']
            self.bg_text.blit(text, textrect)
        
        self.text = data.render_text(data.FONT_MAIN, 37, 'Push the button !', (255, 255, 255))
        self.textrect = self.text.get_rect()
        
#        bg_text.blit(self.text, self.textrect)

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
        y += self.textrect.height * 1.5

    def draw(self, screen):
        screen.blit(self.background, (0, 0))
        
        fontTitle = data.load_font(data.FONT_TITLE, 45)
        fontTitle.set_underline(True)
        title = fontTitle.render('How to play', True, (255, 255, 255))
        titlerect = title.get_rect()
        titlerect.centerx = screen.get_rect().centerx
        titlerect.top = 30
        screen.blit(title, titlerect)
        
        self.bg_textrect.top = 100
        self.bg_textrect.centerx = screen.get_rect().centerx
        screen.blit(self.bg_text, self.bg_textrect)