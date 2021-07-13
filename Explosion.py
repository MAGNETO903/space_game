import pygame

class Explosion:
    def __init__(self, x, y, frame_num, size_x, size_y):
        self.x = x
        self.y = y
        self.frame = frame_num
        self.size_x = size_x
        self.size_y = size_y

    def draw(self, display, frames):
        img = pygame.transform.scale(frames[self.frame], (self.size_x, self.size_y))
        display.blit(img, (self.x, self.y))