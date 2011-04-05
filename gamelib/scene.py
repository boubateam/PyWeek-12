'''The scene class.
'''

class Scene(object):
    '''Represents an abstract scene.
    '''

    name = ''

    def __init__(self, game, name, index, config=None):
        self.game = game
        self.name = name
        self.index = index
        self.config = config

    def start(self):
        pass

    def end(self):
        pass

    def handleEvent(self, event):
        raise NotImplementedError()

    def update(self):
        raise NotImplementedError()

    def draw(self, screen):
        raise NotImplementedError()
