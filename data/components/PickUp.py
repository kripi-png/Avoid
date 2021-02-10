import pygame, random
from ..Scenes import ASSETLOADER
from ..CONSTANTS import WIDTH, HEIGHT

class _PickUp(pygame.sprite.Sprite):
    """Parent class for all pick ups.  no direct _PickUp object should ever be created."""

    def __init__(this):
        super(_PickUp, this).__init__()
        this.image = ASSETLOADER.pickupEmpty
        this.rect = this.image.get_rect()
        this.size = this.image.get_size()

        this.x, this.y = random.randint(0+this.size[0], WIDTH-this.size[0]), random.randint(0+this.size[1], HEIGHT-this.size[1])
        this.rect.center = this.x, this.y
        this.spawnTime = pygame.time.get_ticks()
        this.lifeLongevity = 2000 # how long it takes for the box to disappear

        this.moving = False
        this.speed = None
        this.direction = None


    def update(this):
        if not this.moving: pass
        if pygame.time.get_ticks() - this.spawnTime >= this.lifeLongevity:
            this.kill()

class FireRatePickUp(_PickUp):
    """Boosts the rate of fire for X seconds"""
    def __init__(this):
        super(FireRatePickUp, this).__init__()
        this.image = ASSETLOADER.pickupFirerateUp
        this.effectLongevity = 2000 # ms
        this.effectStrength = 6

    def pickUp(this, target):
        print("firerate buff added")
        target.activeEffects.append({
            "name":"firerateUp",
            "effectApplied": pygame.time.get_ticks(),
            "effectLongevity": this.effectLongevity,
            "effectTargetStat": target.fireRate,
            "effectStrength": this.effectStrength
        })
        target.fireRate += this.effectStrength
        print(target.fireRate)
