'''The scene class.
'''

class Scene(object):
    '''Represents an abstract scene.
    '''

    def __init__(self, game):
        self.game = game

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
