import pygame
from .Bullet import *
from ..Scenes import ASSETLOADER

class Player(pygame.sprite.Sprite):
    def __init__(this, damage, fireRate, scene):
        super(Player, this).__init__()
        this.image = ASSETLOADER.spritePlayer
        this.damage = damage
        this.fireRate = fireRate # in seconds
        this.scene = scene
        this.playerBullets = scene.playerBullets
        this.rect = this.image.get_rect()
        this.size = this.image.get_size()

        this.activeEffects = []

        this.scene.eventManager.addEvent('playerAttackEvent', this.attack, 1000 // this.fireRate)

    def update(this):
        pos = pygame.mouse.get_pos()
        this.rect.center = pos
        this.scene.eventManager.editEvent('playerAttackEvent', this.attack, 1000 // this.fireRate)

        for effect in this.activeEffects:
            # remove effect from the list if it has expired
            if pygame.time.get_ticks() - effect["effectApplied"] >= effect["effectLongevity"]:
                this.fireRate -= effect["effectStrength"]
                this.activeEffects.remove(effect)

    def attack(this):
        this.playerBullets.add(PlayerBullet(this.rect.center, -90, 5)) # +90 because 0 == right

    def kill(this):
        this.scene.eventManager.removeEvent('playerAttackEvent')
        # pygame.time.set_timer(this.specialAttackEvent, 0) # TODO
