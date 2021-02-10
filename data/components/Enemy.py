# basic enemy
# attack: bullet wave
# special attack: homing bullet

import pygame
import math
from random import randint
from .Bullet import *

class Enemy(pygame.sprite.Sprite):
    def __init__(this, health, attacks, image, bulletList, scene, attackSound):
        super(Enemy, this).__init__()
        this.speed = 5
        this.health_capacity = health
        this.current_health = this.health_capacity
        this.attacks = attacks
        this.scene = scene
        this.image, this.bulletList, this.attackSound = image, bulletList, attackSound
        this.rect, this.size = this.image.get_rect(), this.image.get_size()
        this.rect.center = ((1300 - this.size[0])/2, 20 + this.size[1]/2)
        this.velX = -5 if randint(0,1) else 5 # 50/50 chance to go either way
        this.dead = False

        this.scene.eventManager.addEvent('changeDirEvent', this.changeDir, 2000)
        if 'bulletWave' in this.attacks:
            this.scene.eventManager.addEvent('bulletWaveEvent', this.bulletWave, 1000)
        if 'bulletWaveEasy' in this.attacks:
            this.scene.eventManager.addEvent('bulletWaveEasyEvent', this.bulletWaveEasy, 1000)
        if 'homingBulletWave' in this.attacks:
            this.scene.eventManager.addEvent('homingBulletWaveEvent', this.homingBulletWave, 2000)

        this.enemy = scene.player # enemy of the enemies aka the player
                                  # imo makes sense for the bullets to call the player an enemy

    def update(this):
        this.rect.x += this.velX
    def changeDir(this):
        this.velX = -this.speed if randint(0,1) else this.speed
    def forceDir(this):
        this.velX = -this.velX

    def bulletWaveEasy(this):
        this.attackSound.play()
        bc = 6 # bulletCount
        sa = -60 # startingAngle
        for i in range(bc):
            this.bulletList.add(Bullet(this.rect.center, sa + 90, 5)) # +90 because 0 == right
            sa += 120 / bc

    def bulletWave(this):
        this.attackSound.play()
        bc = 12 # bulletCount
        sa = -60 # startingAngle
        for i in range(bc):
            this.bulletList.add(Bullet(this.rect.center, sa + 90, 5)) # +90 because 0 == right
            sa += 120 / bc

    def homingBulletWave(this):
        this.attackSound.play()
        bc = 4 # bulletCount
        sa = -60 # startingAngle
        for i in range(bc):
            this.bulletList.add(HomingBullet(this.rect.center, sa + 90, 7, this.enemy)) # +90 because 0 == right
            sa += 120 / bc

    def damage(this): # take damage
        this.current_health -= this.enemy.damage

    def kill(this):
        this.scene.eventManager.removeEvent('changeDirEvent')
        for atk in this.attacks:
            this.scene.eventManager.removeEvent(atk+'Event')
