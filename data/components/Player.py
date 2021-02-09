import pygame
from .Bullet import Bullet

class Player(pygame.sprite.Sprite):
    def __init__(this, damage, attackSpeed, image, scene):
        super(Player, this).__init__()
        this.image = image
        this.damage = damage
        this.scene = scene
        this.playerBullets = scene.playerBullets
        this.attackSpeed = attackSpeed # in seconds
        this.rect = this.image.get_rect()
        this.size = this.image.get_size()

        this.scene.eventManager.addEvent('playerAttackEvent', this.attack, int(1000 * this.attackSpeed))

    def update(this):
        pos = pygame.mouse.get_pos()
        this.rect.center = pos

    def attack(this):
        this.playerBullets.add(Bullet(this.rect.center, -90, 'playerBullet', 5)) # +90 because 0 == right

    def kill(this):
        this.scene.eventManager.removeEvent('playerAttackEvent')
        # pygame.time.set_timer(this.specialAttackEvent, 0) # TODO
