import os, pygame
folder = os.path.dirname(__file__)

def loadImage(n):
    imgFolder = os.path.join(folder, 'img')
    return pygame.image.load(os.path.join(imgFolder, n+".png"))

def loadSound(n):
    soundFolder = os.path.join(folder, 'audio')
    return pygame.mixer.Sound(os.path.join(soundFolder, n))
