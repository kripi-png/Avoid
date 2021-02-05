import pygame
from pygame.math import Vector2
from random import uniform
from Utils import *

class Bullet(pygame.sprite.Sprite):
    def __init__(this, loc, angle, image, speed):
        super(Bullet, this).__init__()
        this.image = loadImage(image) # loadImage function is located in Utils.py
        this.speed = uniform(speed-.4, speed+.4) # uniform = randint for floats.
                                                # This is to randomize the speeds of bullet in order to make them a bit more unpredictable
        this.rect = this.image.get_rect(center=loc) # loc == the location of the Enemy object
        this.angle = angle
        this.velocity = Vector2(1,0).rotate(this.angle) * this.speed
        this.pos = Vector2(this.rect.center)

    def update(this, dt):
        this.pos += this.velocity
        this.rect.center = this.pos
