import pygame
from Bullet import Bullet


class Player(pygame.sprite.Sprite):
    def __init__(this, damage, attackSpeed, image, playerBullets):
        super(Player, this).__init__()
        this.image = image
        this.damage = damage
        this.playerBullets = playerBullets
        this.attackSpeed = attackSpeed # in seconds
        this.rect = this.image.get_rect()
        this.size = this.image.get_size()

        this.attackEvent = pygame.event.Event(pygame.USEREVENT+4)
        pygame.time.set_timer(this.attackEvent, int(1000 * this.attackSpeed))

    def update(this):
        pos = pygame.mouse.get_pos()
        this.rect.center = pos

    def attack(this):
        this.playerBullets.add(Bullet(this.rect.center, -90, 'playerBullet', 5)) # +90 because 0 == right

    def kill(this):
        pygame.time.set_timer(this.attackEvent, 0)
        # pygame.time.set_timer(this.specialAttackEvent, 0) # TODO
