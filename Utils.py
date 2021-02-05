import os, pygame
folder = os.path.dirname(__file__)

def loadImage(n):
    return pygame.image.load('img/'+n+".png")

def loadSound(n):
    return pygame.mixer.Sound(os.path.join('audio/'+n))
