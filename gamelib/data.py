'''Simple data loader module.

Loads data files from the "data" directory shipped with a game.

Enhancing this to handle caching etc. is left as an exercise for the reader.
'''

import os
import pygame

data_py = os.path.abspath(os.path.dirname(__file__))
data_dir = os.path.normpath(os.path.join(data_py, '..', 'data'))

FONT_TITLE = 'convoy.ttf'
FONT_MAIN = 'DejaVuSans.ttf'
FONT_FIX = 'digitaldream.ttf'

def filepath(filename):
    '''Determine the path to a file in the data directory.
    '''
    return os.path.join(data_dir, filename)

def load(filename, mode='rb'):
    '''Open a file in the data directory.

    "mode" is passed as the second arg to open().
    '''
    return open(os.path.join(data_dir, filename), mode)

def load_image(filename, theme=''):
    '''Return a loaded image.
    '''
    if theme == '':
        return pygame.image.load(filepath(filename)).convert()
    else:
        return pygame.image.load(filepath(os.path.join('themes', theme, filename))).convert()

def load_font(name, size):
    filename = None

    if not name == None:
        filename = filepath(os.path.join('fonts', name))

    return pygame.font.Font(filename, size)

def load_sound(filename, theme=''):
    if theme == '':
        return pygame.mixer.Sound(filepath(filename))
    else:
        return pygame.mixer.Sound(filepath(os.path.join('themes', theme,filename)))

def render_text(fontname, fontsize, text, color):
    font = load_font(fontname, fontsize)
    rend = font.render(text, True, color)

    return rend
