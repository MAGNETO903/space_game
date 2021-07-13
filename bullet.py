import pygame

class Bullet(pygame.sprite.Sprite):
    def __init__(self, x, y, bullet_img):
        pygame.sprite.Sprite.__init__(self)
        #self.image = pygame.transform.scale(pygame.image.load('assets/shot5_asset.png'), (6, 31))
        self.image = bullet_img
        #self.image.fill(laguna)
        self.rect = self.image.get_rect()
        self.rect.bottom = y
        self.rect.centerx = x
        self.speedy = -10

    def update(self, size):
        self.rect.y += self.speedy

        if self.rect.bottom < 0:
            self.kill()
