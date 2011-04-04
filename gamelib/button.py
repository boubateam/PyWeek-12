
import game
import random
import os
import pygame

'''The ButtonSuite class.
'''
class Button(pygame.sprite.Sprite):
    '''Represents an abstract scene.
    '''

    def __init__(self, btnname):
        pygame.sprite.Sprite.__init__(self)
        self.config = {}
        self.btnNameForDebugInLevelWhenUsingBtnList = btnname
        self.image = pygame.Surface([15, 15])
        self.image.fill([255, 0, 0])

        # Make our top-left corner the passed-in location.
        self.rect = self.image.get_rect()
        self.rect.topleft = [0,0]

    def __str__(self):
        return self.btnNameForDebugInLevelWhenUsingBtnList
    
'''The ButtonsList class.
'''
class ButtonsList(object):
    '''Represents an abstract scene.
    '''

    def __init__(self, game):
        
        '''Pas trouve comment definir un tableau sans avoir l\'erreur plus bas.
        me rappellant du malloc(sizeof(laliste)) en c, j'ai stupidement utilise range(0, size)
        mais j'espere que python est plus souple que ca.
        Juan si tu me lis, envoie moi un mail avec la definition correcte.
        '''
        self.buttons = range(0,9)
        self.pathLen = game.difficulty
        self.path = range(0,self.pathLen)
        self.game = game
        
        self.initButtons(9)
        self.initPath(self.pathLen)
        
    def initButtons(self, nbbtn):
        ''' initButtons
        '''        
        for i in range(0, nbbtn):
            self.buttons[i] = Button("btn"+str(i))
        
    def initPath(self, plen):
        ''' useless comment here
        '''
        random.seed()
        for i in range(0, plen):
            idx = random.randint(0, len(self.buttons)-1)
            print "random idx is "+str(idx), "buttons length ="+str(len(self.buttons)), "plen is "+str(plen)
            self.path[i] = self.buttons[idx]
    
    def draw(self):
        print "debug infos draw", self.buttons    
      
    def debug(self):
        print 'HERE '+os.linesep, self.path, "here end", os.linesep
        print self
          
    def __str__(self):
        strx = 'buttons are '+os.linesep
        for i in self.buttons:
            strx=strx+" "+str(i)

        strx+=os.linesep+"path is "+os.linesep
        for i in self.path:
            strx+=str(i)+" "
        return strx
               