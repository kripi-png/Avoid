import pygame
from CONSTANTS import *
from Scenes import SceneManager
from Highscores import Highscores

pygame.init()
pygame.mixer.init()

# constants
DISPLAY = pygame.display.set_mode((WIDTH,HEIGHT))
pygame.display.set_caption("Avoid")

sceneManager = SceneManager() # scene manager for changing scenes (mainmenu, gamescene, gameover)

isRunning = True

while isRunning:
    # scene manager calls the functions of whatever scene is currently active
    sceneManager.scene.handleEvents(pygame.event.get())
    sceneManager.scene.update()
    sceneManager.scene.render(DISPLAY)

    pygame.display.flip()
