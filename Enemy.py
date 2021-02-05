# basic enemy
# attack: bullet wave
# special attack: homing bullet

import pygame
import math
from random import randint
from Bullet import Bullet
from HomingBullet import HomingBullet

class Enemy(pygame.sprite.Sprite):
    def __init__(this, health, image, bulletList, enemy, attackSound):
        super(Enemy, this).__init__()
        this.speed = 5
        this.health_capacity = health
        this.current_health = this.health_capacity
        this.image, this.bulletList, this.attackSound = image, bulletList, attackSound
        this.rect, this.size = this.image.get_rect(), this.image.get_size()
        this.rect.center = ((1300 - this.size[0])/2, 20 + this.size[1]/2)
        this.velX = -5 if randint(0,1) else 5 # 50/50 chance to go either way

        this.changeDirEvent = pygame.event.Event(pygame.USEREVENT+1)
        pygame.time.set_timer(this.changeDirEvent, 2000)
        this.attackEvent = pygame.event.Event(pygame.USEREVENT+2)
        pygame.time.set_timer(this.attackEvent, 1000)
        this.specialAttackEvent = pygame.event.Event(pygame.USEREVENT+3)
        pygame.time.set_timer(this.specialAttackEvent, 2000)

        this.bulletCount = 12
        this.fof = 120 # field of fire (degrees)
        this.bulletAngle = this.fof / this.bulletCount

        this.enemy = enemy # enemy of the enemies aka the player
                            # imo makes sense for the bullets to call the player an enemy

    def update(this):
        this.rect.x += this.velX
    def changeDir(this):
        this.velX = -this.speed if randint(0,1) else this.speed
    def forceDir(this):
        this.velX = -this.velX

    def attack(this):
        this.attackSound.play()
        startingAngle = -this.fof / 2
        for i in range(this.bulletCount):
            this.bulletList.add(Bullet(this.rect.center, startingAngle + 90, 'bullet', 5)) # +90 because 0 == right
            startingAngle += this.bulletAngle

    def specialAttack(this):
        this.attackSound.play()
        startingAngle = -this.fof / 2
        for i in range(4):
            this.bulletList.add(HomingBullet(this.rect.center, startingAngle + 90, 'bulletHoming', 7, this.enemy)) # +90 because 0 == right
            startingAngle += this.fof / 4

    def damage(this): # take damage
        this.current_health -= this.enemy.damage

    def kill(this):
        pygame.time.set_timer(this.changeDirEvent, 0)
        pygame.time.set_timer(this.attackEvent, 0)
        pygame.time.set_timer(this.specialAttackEvent, 0)
