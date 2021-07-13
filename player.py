import pygame
from bullet import Bullet

class Player(pygame.sprite.Sprite):
    def __init__(self, size, player_img):
        pygame.sprite.Sprite.__init__(self)
        #self.image = pygame.transform.scale(pygame.image.load('assets/spaceship_4.png'), (50, 40))
        self.image = player_img
        #self.image.fill(red)
        self.rect = self.image.get_rect()
        self.rect.centerx = size[0] / 2
        self.rect.bottom = size[1] - 10
        self.speedx = 0

    def shoot(self, all_sprites, bullets, bullet_img):
        bullet = Bullet(self.rect.centerx, self.rect.top, bullet_img)
        all_sprites.add(bullet)
        bullets.add(bullet)

    def update(self, size):
        self.rect.x += self.speedx
        self.speedx = 0

        key = pygame.key.get_pressed()

        if key[pygame.K_LEFT]:
            self.speedx = -10

        if key[pygame.K_RIGHT]:
            self.speedx = 10

        if self.rect.right > size[0]:
            self.rect.right = size[0]

        if self.rect.left < 0:
            self.rect.left = 0