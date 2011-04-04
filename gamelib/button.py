
import pygame
import random

class Button(pygame.sprite.Sprite):
    '''The Button class.
    '''

    def __init__(self, name, rect):
        pygame.sprite.Sprite.__init__(self)

        self.btnNameForDebugInLevelWhenUsingBtnList = name

        self.image = pygame.Surface((15, 15))
        self.image.fill((255, 0, 0))

        self.rect = self.image.get_rect()
        self.rect.topleft = rect

    def __str__(self):
        return self.btnNameForDebugInLevelWhenUsingBtnList

class ButtonGroup(pygame.sprite.OrderedUpdates):
    '''Contains buttons.
    '''

    def __init__(self, count=9):
        pygame.sprite.OrderedUpdates.__init__(self)

        x = 40
        y = 320

        for i in range(count):
            x += 40
            self.add(Button(i, (x, y)))

        random.seed()

        self.count = count
        self.sequence = [random.randint(0, count - 1) for i in range(count)]

        print 'sequence:', self.sequence
