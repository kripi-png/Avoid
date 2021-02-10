import pygame, math
from pygame.math import Vector2
from random import uniform
from ..Utils import *
from ..Scenes import ASSETLOADER

class Bullet(pygame.sprite.Sprite):
    def __init__(this, loc, angle, speed):
        super(Bullet, this).__init__()
        this.image = ASSETLOADER.bulletNormal # loadImage function is located in Utils.py
        this.speed = uniform(speed-.4, speed+.4) # uniform = randint for floats.
                                                # This is to randomize the speeds of bullet in order to make them a bit more unpredictable
        this.rect = this.image.get_rect(center=loc) # loc == the location of the Enemy object
        this.angle = angle
        this.velocity = Vector2(1,0).rotate(this.angle) * this.speed
        this.pos = Vector2(this.rect.center)

    def update(this, dt):
        this.pos += this.velocity
        this.rect.center = this.pos

class PlayerBullet(Bullet):
    """docstring for PlayerBullet."""
    def __init__(this, *args):
        super(PlayerBullet, this).__init__(*args)
        this.image = ASSETLOADER.bulletPlayer


class HomingBullet(Bullet):
    def __init__(this, loc, angle, speed, enemy):
        super(HomingBullet, this).__init__(loc, angle, speed)
        this.image = ASSETLOADER.bulletHoming
        this.enemy = enemy
        this.homing = False
        this.timer = 3

    def update(this, dt):
        this.timer -= dt
        if this.timer <= 2.5: this.homing = True
        if this.timer <= 0: this.kill()

        if this.homing: # homing disabled for half a second or so but that's not implemented yet
            this.angle = this.getAngle()
            this.velocity = Vector2(1,0).rotate(this.angle) * this.speed
            this.pos += this.velocity
            this.rect.center = this.pos
        else: super().update(dt)

    def getAngle(this):
        px,py = this.enemy.rect.center # playerX, playerY
        dx,dy = px - this.pos[0], py - this.pos[1]
        angle = math.degrees(math.atan2(dy, dx))
        return angle
