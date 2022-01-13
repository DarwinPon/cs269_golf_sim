import pygame
class Arrow:
    def __init__(self, image, x, y, width, height):
        self.rect = pygame.Rect((x, y), (width, height))
        self.x = x
        self.y = y
        self.width = width
        self.height = height
        self.image = pygame.transform.scale(image, (width, height))
        self.rot_img = image
        self.rot_rect = self.rect.copy()
        self.is_visible = True

    def get_rect(self):
        return self.rect

    def set_rot(self, rot_img, rot_x, rot_y):
        self.rot_img = rot_img
        self.rot_rect.x = rot_x
        self.rot_rect.y = rot_y

    def reset(self, ball):
        self.x = ball.rect.x-ball.width
        self.y = ball.rect.y-ball.height
        self.rot_img = self.image.copy()
        self.rect.x = self.x
        self.rect.y = self.y
        self.rot_rect = self.rect.copy()
        self.is_visible = True




