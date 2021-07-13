import pygame
import random

class Enemy(pygame.sprite.Sprite):
    def __init__(self, size, img, enemy_type, x='none', y='none'):
        pygame.sprite.Sprite.__init__(self)
        #self.image = pygame.Surface((30, 40))
        self.image = img
        #if enemy_type == 1:
        #    self.image = pygame.transform.scale(pygame.image.load('assets/enemy.png'), (40, 30))
        #self.image.fill(green)
        self.rect = self.image.get_rect()
        if x == 'none':
            self.rect.x = random.randrange(size[0] - self.rect.width)
        else:
            self.rect.x = x

        if y == 'none':
            self.rect.y = random.randrange(0, 20)
        else:
            self.rect.y = y

        self.speedx = random.randrange(-2, 3)
        self.speedy = random.randrange(1, 5)
        self.type = enemy_type
        self.hp = enemy_type

    def update(self, size):
        self.rect.y += self.speedy
        self.rect.x += self.speedx

        if self.rect.left < 0:
            self.rect.left = 0
            self.speedx = random.randrange(1, 3)

        if self.rect.right > size[0]:
            self.rect.right = size[0]
            self.speedx = random.randrange(-2, 0)

        if self.rect.top < 0:
            self.rect.top = 0
            self.speedy = random.randrange(1, 5)

        if self.rect.bottom > size[1]:
            self.rect.bottom = size[1]
            self.speedy = random.randrange(-5, 0)