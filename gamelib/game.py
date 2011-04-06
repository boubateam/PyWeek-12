'''The game logic.
'''

import pygame
import director

from intro import IntroScene
from menu import MainMenuScene, PauseMenuScene
from credits import CreditsScene
from level import LevelScene
from gameover import GameOverScene
from topscore import TopScoreScene

class Game(object):
    '''Manage the general game logic.
    '''

    def __init__(self):
        self.level  = None
        self.difficulty = 4
        self.points = 0
        self.director = director.Director(self, {
            'title' : 'PyGame',
            'show_fps' : True})

    def run(self):
        self.initLevels()
        self.director.change('intro')
        self.director.run()

    def end(self):
        self.director.end()

    def initLevels(self):
        self.director.register('intro', IntroScene)
        self.director.register('menu', MainMenuScene)
        self.director.register('alien-meeting', LevelScene, {'count': 9, 'delta': 1000, 'pointsMulti': 1})
        self.director.register('alien-chat', LevelScene, {'count': 9, 'delta': 750, 'pointsMulti': 2})
        self.director.register('alien-war', LevelScene, {'count': 9, 'delta': 350, 'pointsMulti': 3})
        self.director.register('credits', CreditsScene)
        self.director.register('gameover', GameOverScene)
        self.director.register('pause', PauseMenuScene)
        self.director.register('topscore', TopScoreScene)
