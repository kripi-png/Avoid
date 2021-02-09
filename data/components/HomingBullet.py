import pygame, math
from pygame.math import Vector2
from .Bullet import Bullet

class HomingBullet(Bullet):
    def __init__(this, loc, angle, image, speed, enemy):
        super(HomingBullet, this).__init__(loc, angle, image, speed)
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
