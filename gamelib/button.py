
import pygame
import random
import data

class Button(pygame.sprite.Sprite):
    '''The Button class.
    '''

    def __init__(self, name, size, position):
        pygame.sprite.Sprite.__init__(self)

        self.name = name
        self.image = pygame.Surface(size)

        self.rect = self.image.get_rect()
        self.rect.topleft = position

        self.active = False

    def associateTheme(self, theme):
        self.sound = data.load_sound('button-' + str(1+self.name) + '.ogg', theme)
        self.sound.set_volume(0.4) 

    def update(self):
        if self.active:
            self.image.fill((0, 0, 255))
            self.sound.play()
        else:
            self.image.fill((255, 0, 0))
            self.sound.stop()

class ButtonGroup(pygame.sprite.OrderedUpdates):
    '''Contains buttons.
    '''

    def __init__(self, size, position, space, count=9, delta=750):
        pygame.sprite.OrderedUpdates.__init__(self)

        x = position[0]
        y = position[1]

        for i in range(count):
            self.add(Button(i, size, (x, y)))
            x += size[0] + space

        self.count = count

        self.animating = False
        self.animTime = 0
        self.animDelta = delta
        self.active = None

    def associateTheme(self, theme):
        self.theme = theme

        for button in self:
            button.associateTheme(self.theme)

    def get(self, index):
        i = 0

        for button in self:
            if i == index:
                return button
            i += 1

        return None

    def update(self):
        if self.animating:
            if pygame.time.get_ticks() > self.animTime:
                self.animating = False
                self.animTime = 0
                self.animateEnd()

        pygame.sprite.OrderedUpdates.update(self)

    def animate(self, button):
        self.animating = True
        self.animTime = pygame.time.get_ticks() + self.animDelta
        self.active = button
        self.active.active = True

    def animateEnd(self):
        self.active.active = False
        self.active = None

class SequenceButtonGroup(ButtonGroup):
    def __init__(self, size, position, space, count=9, delta=750):
        ButtonGroup.__init__(self, size, position, space, count, delta)

        self.sequence = [random.randint(0, count - 1) for i in range(count)]

        self.animateSequence = []
        self.animateCallback = None

    def play(self, number, callback):
        self.animateSequence = self.sequence[:number]
        self.animateCallback = callback
        self.animateNext()

    def validate(self, index):
        return False

    def update(self):
        ButtonGroup.update(self)

    def animateNext(self):
        if len(self.animateSequence) > 0:
            index = self.animateSequence.pop(0)
            button = self.get(index)

            if button:
                self.animate(button)
            else:
                raise IndexError('Button %d not found' % (index, ))
        else:
            self.animateCallback()
            self.animateCallback = None
            self.animateSequence = []

    def animateEnd(self):
        ButtonGroup.animateEnd(self)
        self.animateNext()

class PlayableButtonGroup(ButtonGroup):
    def __init__(self, size, position, space, count=9, delta=750):
        ButtonGroup.__init__(self, size, position, space, count, delta)

    def click(self, pos):
        if not self.animating:
            for index in range(self.count):
                button = self.get(index)

                if button.rect.collidepoint(pos):
                    self.animate(button)
                    return index

        return None

    def update(self):
        ButtonGroup.update(self)
