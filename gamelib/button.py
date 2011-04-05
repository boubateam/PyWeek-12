
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

    def associateTheme(self,theme):
        print('associate theme button-'+ str(1+self.name) + '.ogg')
        self.sound = data.load_sound('button-'+ str(1+self.name) + '.ogg',theme)
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

    def __init__(self, size, position, space, count=9):
        pygame.sprite.OrderedUpdates.__init__(self)

        x = position[0]
        y = position[1]

        for i in range(count):
            self.add(Button(i, size, (x, y)))
            x += size[0] + space

        self.count = count

        self.animating = 0
        self.active = None
    
    def associateTheme(self,theme):
        self.theme = theme
         
        for i in range(self.count):
            button = self.get(i)
            button.associateTheme(self.theme)
        
    def get(self, index):
        buttons = self.sprites()

        try:
            return buttons[index]
        except IndexError:
            return None

    def update(self):
        if not self.active:
            self.animating = 0
        elif self.animating == 0:
            self.active.active = False
            self.active = None
        else:
            self.active.active = True
            self.animating -= 1

        pygame.sprite.OrderedUpdates.update(self)

    def animate(self, button):
        self.active = button
        self.animating = 40
        

class SequenceButtonGroup(ButtonGroup):
    def __init__(self, size, position, space, count=9):
        ButtonGroup.__init__(self, size, position, space, count)

        self.sequence = [random.randint(0, count - 1) for i in range(count)]
        print self.sequence
        #clone so sequence can be used next to check if user clicks is the good result
        self.popableSequence = self.sequence
        self.prevPoppedIdx = None
        self.currentBtnIdx = None
        self.seqDisplayRate = 20
        self.seqDisplayRateCounter = self.seqDisplayRate


    
    def validate(self, play):
        for i in range(len(play)):
            if self.sequence[i] != play[i]:
                return False

        return True
        
    def notifySequencePlayed(self):
        print "sequence played"
        #todo what should be done now ?
    
    def changeButton(self):

        try:
            self.currentBtnIdx = self.popableSequence.pop(0)
        except IndexError:
            self.notifySequencePlayed()

        buttons = self.sprites()

        try:
            buttons[self.currentBtnIdx].active = True  
            if not self.prevPoppedIdx == None:
                buttons[self.prevPoppedIdx].active = False 
        except IndexError:
            pass
        
        self.prevPoppedIdx = self.currentBtnIdx

    def update(self):
        
        if  self.seqDisplayRateCounter == 0:
            self.changeButton()
            self.seqDisplayRateCounter = self.seqDisplayRate    
        else:
            self.seqDisplayRateCounter -= 1
        
        ButtonGroup.update(self)

class PlayableButtonGroup(ButtonGroup):
    def __init__(self, size, position, space, count=9):
        ButtonGroup.__init__(self, size, position, space, count)

    def click(self, event):
        if self.animating == 0: # One button a la fois
            for index in range(self.count):
                button = self.get(index)

                if button.rect.collidepoint(event.pos):
                    self.animate(button)
                    return index

        return None

    def update(self):
        ButtonGroup.update(self)
