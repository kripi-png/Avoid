from .Utils import *

class AssetLoader(object):
    def __init__(this):
        super(AssetLoader, this).__init__()
        print("Loading Images")
        this.spriteBossEyeBlue = loadImage("spriteBossEyeBlue.png")
        this.spritePlayer = loadImage("spritePlayer.png")

        this.bulletNormal = loadImage("bulletNormal.png")
        this.bulletHoming = loadImage("bulletHoming.png")
        this.bulletPlayer = loadImage("bulletPlayer.png")

        this.pickupEmpty = loadImage("pickupEmpty.png")
        this.pickupFirerateUp = loadImage("pickupFirerateUp.png")
        print("Loading Sounds"); print("\n")
        this.hitSound = loadSound("hitSound.ogg")
        this.menuClickSound = loadSound("menuClick.ogg")
        this.soundAttackWaveEnemy = loadSound("bulletWave.ogg")
