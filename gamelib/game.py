'''The great director class.
'''

import pygame
import director

from intro import IntroScene

class Game(object):
    '''Manage the general game logic.
    '''
    def __init__(self):
        self.level  = None
        self.points = 0
        self.director = director.Director({
            'title' : 'PyGame',
            'show_fps' : True})
        

        
    def run(self):
        self.initLevels()
        self.director.change('intro')
        self.director.run()
        
    def end(self):
        self.director.end()
        
    def initLevels(self):
        self.director.register('intro', IntroScene(self))
        
    def sceneEnd(self):
        pass
