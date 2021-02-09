import os, pygame, json

def loadImage(n):
    return pygame.image.load('assets/img/'+n+".png")

def loadSound(n):
    return pygame.mixer.Sound('assets/audio/'+n)

def readLevelsFile():
    with open("data/levels.json") as file:
        return json.load(file)

def formatTime(time):
    s = (time/1000)%60
    s = str(int(s)).rjust(2,'0')
    m =(time/(1000*60))%60
    m = str(int(m)).rjust(2,'0')

    return "{}:{}".format(m,s)
