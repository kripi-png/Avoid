from .Utils import *

class AssetLoader(object):
    def __init__(this):
        super(AssetLoader, this).__init__()

        print("Loading Images")
        this.imageEnemy = loadImage("eyeBoss")
        this.imageEnemyAaro = loadImage("aaroBoss")
        this.imagePlayer = loadImage("player")
        print("Loading Sounds"); print("\n")
        this.hitSound = loadSound("hitSound.ogg")
        this.soundAttackWaveEnemy = loadSound("bulletWave.ogg")
