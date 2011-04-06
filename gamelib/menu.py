
import pygame
import scene
import data

class Menu(pygame.surface.Surface):
    '''Menu
    '''

    def __init__(self, size, menus):
        pygame.surface.Surface.__init__(self, size)

        self.menus = menus
        self.current = 0

        self.menu = None
        self.menurect = None

        self.font = data.load_font('convoy.ttf', 45)
        self.set_colorkey((0, 0, 0)) # Transparent background

    def update(self):
        top = 0

        for i in range(len(self.menus)):
            text, action = self.menus[i]
            color = (255, 255, 255)

            if self.current == i:
                color = (255, 255, 0)

            self.menu = self.font.render(text, True, color)
            self.menurect = self.menu.get_rect()
            self.menurect.centerx = self.get_rect().centerx
            self.menurect.top = top

            top = top + self.menurect.height * 1.5

            self.blit(self.menu, self.menurect)

    def prev(self):
        self.current = self.current - 1

        if self.current < 0:
            self.current = len(self.menus) - 1

    def next(self):
        self.current = self.current + 1

        if self.current >= len(self.menus):
            self.current = 0

    def execute(self):
        text, action = self.menus[self.current]
        action()

class MenuScene(scene.Scene):
    '''Menu Scene
    '''

    def __init__(self, game, name, index, config, size, menus):
        scene.Scene.__init__(self, game, name, index, config)

        self.menu = Menu(size, menus)
        self.menurect = self.menu.get_rect()

    def handleEvent(self, event):
        if event.type == pygame.KEYDOWN:
            if event.key == pygame.K_UP:
                self.menu.prev()
            elif event.key == pygame.K_DOWN:
                self.menu.next()
            elif event.key in [ pygame.K_RETURN, pygame.K_SPACE]:
                self.menu.execute()

    def update(self):
        self.menu.update()

    def draw(self, screen):
        self.menurect.centerx = screen.get_rect().centerx
        self.menurect.centery = screen.get_rect().centery

        screen.blit(self.menu, self.menurect)

class MainMenuScene(MenuScene):
    '''Main Menu
    '''

    def __init__(self, game, name, index, config=None):
        self.background = data.load_image('menu.png')

        menus = (('Start Game', self.play),
                 ('Credits', self.credits),
                 ('Exit', self.exit))

        MenuScene.__init__(self, game, name, index, config, (320, 240), menus)
        self.music_bg = data.load_sound('menu.ogg')
        self.music_bg.set_volume(0.4)
    
    def start(self):
        self.music_bg.play(fade_ms=1000)
        
    def end(self):
        self.music_bg.fadeout(1000)

        
    def play(self):
        self.game.director.endScene(True)

    def credits(self):
        self.game.director.changeAndBack('credits')

    def exit(self):
        self.game.end()

    def draw(self, screen):
        screen.blit(self.background, (0, 0))
        super(MainMenuScene, self).draw(screen)

class PauseMenuScene(MenuScene):
    '''Pause Menu
    '''

    def __init__(self, game, name, index, config=None):
        self.background = pygame.surface.Surface((640, 480), flags=pygame.SRCALPHA)
        self.background.fill((0, 0, 0, 95))

        menus = (('Resume', self.cont),
                 ('Back to Menu', self.back))

        MenuScene.__init__(self, game, name, index, config, (320, 240), menus)
        self.music_bg = data.load_sound('pause.ogg')

    def start(self):
        self.music_bg.play()
        self.backgrounded = False

    def cont(self):
        self.game.director.endScene()

    def back(self):
        self.game.director.change('menu')

    def draw(self, screen):
        if not self.backgrounded:
            screen.blit(self.background, (0, 0))
            self.backgrounded = True

        super(PauseMenuScene, self).draw(screen)
