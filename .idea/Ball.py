import pygame
class Ball:
    def __init__(self, image, x, y, width, height, vel_x, vel_y):
        self.rect = pygame.Rect((x, y), (width, height))
        self.x = x
        self.y = y
        self.width = width
        self.height = height
        self.image = pygame.transform.scale(image, (width, height))
        self.vel_x = vel_x
        self.vel_y = vel_y

    def get_rect(self):
        return self.rect


