'''Game main module.

Contains the entry point used by the run_game.py script.

Feel free to put all your game code here, or in other modules in this "gamelib"
package.
'''

import pygame
import game

def main():
    pygame.init();

    g = game.Game()
    g.run()
