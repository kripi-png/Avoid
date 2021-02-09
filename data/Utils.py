import os, pygame, json

def loadImage(n):
    return pygame.image.load('assets/img/'+n+".png")

def loadSound(n):
    return pygame.mixer.Sound('assets/audio/'+n)

def readLevelsFile():
    with open("data/levels.json") as file:
        return json.load(file)
