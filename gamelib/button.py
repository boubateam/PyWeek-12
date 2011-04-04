
import pygame
import random

class Button(pygame.sprite.Sprite):
    '''The Button class.
    '''

    def __init__(self, name, size, position):
        pygame.sprite.Sprite.__init__(self)

        self.btnNameForDebugInLevelWhenUsingBtnList = name

        self.image = pygame.Surface(size)

        self.rect = self.image.get_rect()
        self.rect.topleft = position

        self.active = False

    def update(self):
        if self.active:
            self.image.fill((0, 0, 255))
        else:
            self.image.fill((255, 0, 0))

    def __str__(self):
        return self.btnNameForDebugInLevelWhenUsingBtnList

class ButtonGroup(pygame.sprite.OrderedUpdates):
    '''Contains buttons.
    '''

    def __init__(self, size, position, space, count=9):
        pygame.sprite.OrderedUpdates.__init__(self)

        x = position[0]
        y = position[1]

        for i in range(count):
            self.add(Button(i, size, (x, y)))
            x += size[0] + space

        self.count = count

class SequenceButtonGroup(ButtonGroup):
    def __init__(self, size, position, space, count=9):
        ButtonGroup.__init__(self, size, position, space, count)

        self.sequence = [random.randint(0, count - 1) for i in range(count)]
        print 'sequence:', self.sequence

class PlayableButtonGroup(ButtonGroup):
    def __init__(self, size, position, space, count=9):
        ButtonGroup.__init__(self, size, position, space, count)

        self.animating = 0

    def click(self, event):
        if self.animating == 0: # One button a la fois
            for button in self:
                if button.rect.collidepoint(event.pos):
                    button.active = True
                    self.animating = 40

    def update(self):
        ButtonGroup.update(self)

        if self.animating == 0:
            for button in self:
                button.active = False
        else:
            self.animating -= 1
