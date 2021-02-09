from .Utils import *

class AssetLoader(object):
    def __init__(this):
        super(AssetLoader, this).__init__()

        print("Loading Images")
        this.imageEnemyEye = loadImage("eyeBoss")
        this.imagePlayer = loadImage("player")
        print("Loading Sounds"); print("\n")
        this.hitSound = loadSound("hitSound.ogg")
        this.menuClickSound = loadSound("menuClick.ogg")
        this.soundAttackWaveEnemy = loadSound("bulletWave.ogg")
