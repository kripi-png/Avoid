import pygame
from .CONSTANTS import *
from .Highscores import Highscores

# initialize stuff before starting the game
pygame.init()
pygame.mixer.init()

from .Scenes import SceneManager

def main():
    # constants
    DISPLAY = pygame.display.set_mode((WIDTH,HEIGHT))
    pygame.display.set_caption("Avoid")
    sceneManager = SceneManager() # scene manager for changing scenes (mainmenu, gamescene, gameover)

    while True:
        # scene manager calls the functions of whatever scene is currently active
        sceneManager.scene.handleEvents(pygame.event.get())
        sceneManager.scene.update()
        sceneManager.scene.render(DISPLAY)

        pygame.display.flip()
