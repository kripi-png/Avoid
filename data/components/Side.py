import pygame

class Side(pygame.sprite.Sprite):
    def __init__(this, x, y, w, h):
       pygame.sprite.Sprite.__init__(this)
       this.image = pygame.Surface([w, h])
       this.image.fill(0xffffff)
       this.rect = this.image.get_rect()
       this.rect.x, this.rect.y = x, y
