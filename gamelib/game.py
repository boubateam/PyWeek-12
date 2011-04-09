'''The game logic.
'''

import pygame
import director
import data

from intro import IntroScene
from menu import MainMenuScene, PauseMenuScene
from credits import CreditsScene
from howto import HowtoScene
from level import LevelScene
from gameover import GameOverScene

class Game(object):
    '''Manage the general game logic.
    '''

    def __init__(self):
        self.level  = None
        self.difficulty = 4
        self.points = 0
        self.director = director.Director(self, {
            'title' : 'Ninth Kind',
            'show_fps' : False})
        self.music = data.load_sound('intro.ogg')
        self.channel = None

    def run(self):
        self.initLevels()
        self.director.change('intro')
        self.director.run()

    def end(self):
        self.director.end()

    def initLevels(self):
        self.director.register('intro', IntroScene)
        self.director.register('menu', MainMenuScene)
        self.director.register('alien-meeting', LevelScene, {'count': 9, "volume":0.3, "timetoclick": 200, 'delta': 1000, 'pointsMulti': 1 })
        self.director.register('alien-chat', LevelScene, {'count': 9, "volume":0.8, "timetoclick": 100, 'delta': 750, 'pointsMulti': 2 })
        self.director.register('alien-war', LevelScene, {'count': 9, "volume":1, "timetoclick": 50, 'delta': 350, 'pointsMulti': 3 })
        self.director.register('youwin', GameOverScene, {'message':'Congratulations !','music':'credits.ogg'})
        self.director.register('credits', CreditsScene)
        self.director.register('howto', HowtoScene)
        self.director.register('gameover', GameOverScene, {'message':'Game Over'})
        self.director.register('pause', PauseMenuScene)
