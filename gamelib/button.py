
import pygame
import random
import data

class Button(pygame.sprite.Sprite):
    '''The Button class.
    '''

    def __init__(self, name, size, position, diff):
        pygame.sprite.Sprite.__init__(self)

        self.name = name

        self.origImage = pygame.Surface(size, flags=pygame.SRCALPHA)
        self.origRect = pygame.Rect(position, size)

        self.image = self.origImage
        self.rect = self.origRect

        self.activeImage = None
        self.activeRect = pygame.Rect(
            (position[0] - diff, position[1] - diff),
            (size[0] + diff * 2, size[1] + diff * 2))

        self.active = False

    def associateTheme(self, type, theme):
        self.activeImage = data.load_image('button-' + type + '-' + str(1+self.name) + '.png')
        self.sound = data.load_sound('button-' + type + '-' + str(1+self.name) + '.ogg', theme)
        self.sound.set_volume(0.4)
        self.channel = None 

    def update(self):
        if self.active:
            self.image = self.activeImage
            self.rect = self.activeRect
            
            if self.channel == None:
                self.channel = self.sound.play()
        else:
            self.image = self.origImage
            self.rect = self.origRect

            if self.channel != None:
                if not self.channel.get_busy():
                    self.channel = None

class ButtonGroup(pygame.sprite.OrderedUpdates):
    '''Contains buttons.
    '''

    def __init__(self, size, position, diff, space, count=9, delta=750):
        pygame.sprite.OrderedUpdates.__init__(self)

        x = position[0]
        y = position[1]

        for i in range(count):
            self.add(Button(i, size, (x, y), diff))
            x += size[0] + space

        self.count = count

        self.animating = False
        self.animTime = 0
        self.animDelta = delta
        self.active = None

        self.wait = False
        self.waitTime = 0


    def get(self, index):
        i = 0

        for button in self:
            if i == index:
                return button
            i += 1

        return None

    def update(self):
        if self.animating and  pygame.time.get_ticks() > self.animTime:
            self.animating = False
            self.animTime = 0
            self.animateEnd()

        if self.wait and pygame.time.get_ticks() > self.waitTime:
            self.waitEnd()
            self.waitExec()

        pygame.sprite.OrderedUpdates.update(self)

    def waitStart(self):
        self.wait = True
        self.waitTime = pygame.time.get_ticks() + self.animDelta

    def waitEnd(self):
        self.wait = False
        self.waitTime = 0

    def waitExec(self):
        pass

    def animate(self, button):
        self.animating = True
        self.animTime = pygame.time.get_ticks() + self.animDelta
        self.active = button
        self.active.active = True

    def animateEnd(self):
        if not self.active.channel == None:
            self.active.channel.stop()
            self.active.channel = None
        self.active.active = False
        self.active = None

class SequenceButtonGroup(ButtonGroup):
    def __init__(self, size, position, diff, space, count=9, delta=750,delta_next=200):
        ButtonGroup.__init__(self, size, position, diff, space, count, delta)

        self.sequence = [random.randint(0, count - 1) for i in range(count)]

        self.animateSequence = []
        self.animateCallback = None

        self.waitNext = False
        self.waitNextTime = 0
        self.deltaNext = delta_next

        self.played = False

    def associateTheme(self,  theme):
        self.theme = theme

        for button in self:
            button.associateTheme('sequence' ,self.theme)

    def play(self, number, callback):
        self.animateSequence = self.sequence[:number]
        self.animateCallback = callback
        self.waitStart()

    def waitExec(self):
        self.animateNext()

    def validate(self, play):
        for i in range(len(play)):
            if self.sequence[i] != play[i]:
                return False
        return True

    def update(self):
        if not self.waitNext:
            ButtonGroup.update(self)
        elif self.waitNext and pygame.time.get_ticks() > self.waitNextTime:
            self.waitNextEnd()

    def waitNextStart(self):
        self.waitNext = True
        self.waitNextTime = pygame.time.get_ticks() + self.deltaNext

    def waitNextEnd(self):
        self.waitNext = False
        self.waitNextTime = 0
        self.animateNext()

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
        self.waitNextStart()

class PlayableButtonGroup(ButtonGroup):
    def __init__(self, size, position, diff, space, count=9, delta=750):
        ButtonGroup.__init__(self, size, position, diff, space, count, delta)

    def associateTheme(self,  theme):
        self.theme = theme

        for button in self:
            button.associateTheme('playable' ,self.theme)

    def click(self, pos):
        if not self.animating:
            for index in range(self.count):
                button = self.get(index)

                if button.rect.collidepoint(pos):
                    self.animate(button)
                    return index

        return None

    def push(self, index):
        if not self.animating:
            button = self.get(index)
            self.animate(button)
            return index
        return None

    def update(self):
        ButtonGroup.update(self)
