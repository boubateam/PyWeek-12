
import pygame
import scene

class Menu(pygame.surface.Surface):
    '''Menu
    '''

    def __init__(self, size, menus):
        pygame.surface.Surface.__init__(self, size)

        self.menus = menus
        self.current = 0

        self.current = None
        self.currentrect = None

        self.set_colorkey((0, 0, 0)) # Transparent background

    def update(self):
        top = 0

        for i in range(len(self.menus)):
            text, action = self.menus[i]
            fontcolor = (255, 255, 255)

            if self.current == i:
                fontcolor = (255, 255, 0)

            self.current, self.currentrect = self._create(text, fontcolor)
            self.currentrect.centerx = self.get_rect().centerx
            self.currentrect.top = top

            top = top + self.currentrect.height * 1.5

            self.blit(self.current, self.currentrect)

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

    def _create(self, text, fontcolor=None):
        font = pygame.font.Font(None, 37)
        rend = font.render(text, False, fontcolor or (255, 255, 255))

        return rend, rend.get_rect()

class MenuScene(scene.Scene):
    '''Menu Scene
    '''

    def __init__(self, game, size, menus):
        scene.Scene.__init__(self, game)

        self.menu = Menu(size, menus)
        self.menurect = self.menu.get_rect()

    def start(self):
        pass

    def end(self):
        pass

    def handleEvent(self, event):
        if event.type == pygame.KEYDOWN:
            if event.key == pygame.K_UP:
                self.menu.prev()
            elif event.key == pygame.K_DOWN:
                self.menu.next()
            elif event.key == pygame.K_RETURN:
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

    def __init__(self, game):
        menus = (('Start Game', self.play),
                 ('Exit', self.exit))

        MenuScene.__init__(self, game, (320, 240), menus)

    def play(self):
        self.game.director.change('game')

    def exit(self):
        self.game.end()
