'''The scene class.
'''

class Scene(object):
    '''Represents an abstract scene.
    '''

    def __init__(self, director):
        self.director = director

    def changed(self):
        raise NotImplementedError()

    def event(self, event):
        raise NotImplementedError()

    def update(self):
        raise NotImplementedError()

    def draw(self, screen):
        raise NotImplementedError()
