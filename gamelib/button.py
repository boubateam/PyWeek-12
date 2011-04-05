
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

        self.animating = False
        self.animTime = 0
        self.active = None

    def associateTheme(self, theme):
        self.theme = theme

        for button in self:
            button.associateTheme(self.theme)

    def get(self, index):
        buttons = self.sprites()

        try:
            return buttons[index]
        except IndexError:
            return None

    def update(self):
        if self.animating:
            if pygame.time.get_ticks() > self.animTime:
                self.animating = False
                self.animTime = 0
                self.active.active = False
                self.active = None

        pygame.sprite.OrderedUpdates.update(self)

    def animate(self, button):
        self.animating = True
        self.animTime = pygame.time.get_ticks() + 750
        self.active = button
        self.active.active = True

class SequenceButtonGroup(ButtonGroup):
    def __init__(self, size, position, space, count=9):
        ButtonGroup.__init__(self, size, position, space, count)

        self.sequence = [random.randint(0, count - 1) for i in range(count)]
        print "sequence is "
        print self.sequence

        self.popableSequence = self.sequence[:]
        self.userValidatingSeq = self.sequence[:]        
        self.prevPoppedIdx = None
        self.currentBtnIdx = None
        self.seqDisplayTimeRate = 1000
        self.seqDisplayRateCounter = 0
        self.playing = True
        self.buttons = self.sprites()

    def validate(self, clickedBtnIdx):
        
        if self.userValidatingSeq.pop(0) == clickedBtnIdx :
            return True
        else:
            return False

    def notifySequencePlayed(self):
        print "sequence played"
        self.playing = False
        #todo what should be done now ?

    def changeButton(self):
        
        try:
            self.currentBtnIdx = self.popableSequence.pop(0)
        except IndexError:
            self.buttons[self.prevPoppedIdx].active = False 
            self.notifySequencePlayed()
            return

        print "playing button "+str(self.currentBtnIdx), "prev idx =", str(self.prevPoppedIdx)
        
        #Etrangement, le code suivant ne fonctionne pas (button semble etre une copie au lieu d'une ref)
        '''        
button = self.get(self.currentBtnIdx)
        button.active = True
        
        if not self.prevPoppedIdx == None:
            button.active = False 
            '''
        try:
            if not self.prevPoppedIdx == None:
                self.buttons[self.prevPoppedIdx].active = False 
            
            self.buttons[self.currentBtnIdx].active = True     
        except IndexError:
            pass


        self.prevPoppedIdx = self.currentBtnIdx

    def update(self):
        if  self.playing and pygame.time.get_ticks() > self.seqDisplayRateCounter:
            self.changeButton()
            self.seqDisplayRateCounter = pygame.time.get_ticks() + self.seqDisplayTimeRate
            
            
        ButtonGroup.update(self)

class PlayableButtonGroup(ButtonGroup):
    def __init__(self, size, position, space, count=9):
        ButtonGroup.__init__(self, size, position, space, count)

    def click(self, pos):
        if not self.animating: # One button a la fois
            for index in range(self.count):
                button = self.get(index)

                if button.rect.collidepoint(pos):
                    self.animate(button)
                    return index

        return None

    def update(self):
        ButtonGroup.update(self)
