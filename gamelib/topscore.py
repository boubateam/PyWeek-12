'''The game over scene.
'''

import pygame
import scene
import data
import string

class TopScoreScene(scene.Scene):
    def __init__(self, game, name, index, config=None):
        super(TopScoreScene, self).__init__(game, name, index, config)

        self.text = data.render_text('LiberationSans-Regular.ttf', 17, 'Who\'s the rockstar with 1000 points ?', (255, 255, 255))
        self.textrect = self.text.get_rect()
        
        #temp
        self.textInputRect = self.textrect
        
        self.music_bg = data.load_sound('intro.ogg')
        self.background = data.load_image('intro.png')
        self.userFilledStr = []
        self.usernickText = None
        self.userFillingTextField = False
        
    def start(self):
        self.music_bg.play()
    
    def end(self):
        self.music_bg.fadeout(1000)
        
    def handleEvent(self, event):
        
        if event.type == pygame.MOUSEBUTTONUP:
            if self.textInputRect.collidepoint(event.pos):
                self.userFillingTextField = True
            
        if event.type == pygame.KEYDOWN:
            
            if not self.userFillingTextField and event.key == pygame.K_ESCAPE:
                self.game.director.change('menu')
                
            if self.userFillingTextField:
                if event.key == pygame.K_BACKSPACE:
                    self.userFilledStr = self.userFilledStr[0:-1]
                elif event.key == pygame.K_RETURN or event.key == pygame.K_ESCAPE:
                    self.userFillingTextField = False
                elif event.key == pygame.K_MINUS:
                    self.userFilledStr.append("_")
                elif event.key <= 127:
                    self.userFilledStr.append(chr(event.key))


    def update(self):
        self.usernickText = data.render_text('genotype.ttf', 17, string.join(self.userFilledStr), (255, 255, 255))
        self.usernickTextRect = self.text.get_rect()
        self.textrect.center = (320, 20)
        self.usernickTextRect.center = (320, 50)

    def draw(self, screen):
        screen.blit(self.background, (0, 0))
        screen.blit(self.text, self.textrect)
        screen.blit(self.usernickText, self.usernickTextRect)