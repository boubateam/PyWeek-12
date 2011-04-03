'''Game main module.

Contains the entry point used by the run_game.py script.

Feel free to put all your game code here, or in other modules in this "gamelib"
package.
'''

import pygame
import director

from intro import IntroScene

def main():
    pygame.init();

    g = director.Director({
        'title' : 'PyGame',
        'show_fps' : True})
    g.register('intro', IntroScene)
    g.change('intro')
    g.run()
