import pygame, random
from ..Scenes import ASSETLOADER
from ..CONSTANTS import WIDTH, HEIGHT

class _Pickup(pygame.sprite.Sprite):
    """Parent class for all pick ups. No direct _Pickup object should ever be created."""

    def __init__(this):
        super(_Pickup, this).__init__()
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

class FirerateUpPickup(_Pickup):
    """Boosts the rate of fire for X seconds"""
    def __init__(this):
        super(FirerateUpPickup, this).__init__()
        this.image = ASSETLOADER.pickupFirerateUp
        this.effectLongevity = 2000 # ms
        this.effectStrength = 6

    def pickUp(this, target):
        target.fireRate += this.effectStrength
        target.activeEffects.append({
            "name":"firerateUp",
            "effectApplied": pygame.time.get_ticks(),
            "effectLongevity": this.effectLongevity,
            "effectTargetStat": target.fireRate,
            "effectStrength": this.effectStrength
        })
