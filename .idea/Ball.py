
import pygame
import math
class Ball:
    def __init__(self, image, x, y, width, height, arrow):
        self.rect = pygame.Rect((x, y), (width, height))
        self.x = x
        self.y = y
        self.width = width
        self.height = height
        self.image = pygame.transform.scale(image, (width, height))
        self.vel = 0
        self.acc = 0.25
        self.angle = 0
        self.launchF = 0
        self.arrow = arrow
        self.RADIUS = 15

    def get_rect(self):
        return self.rect

    def get_x(self):
        return self.rect.x

    def get_y(self):
        return self.rect.y

    def get_radius(self):
        return self.RADIUS

    def set_rot(self, rot_img, rot_rect):
        self.rot_img = rot_img
        self.rot_rect = rot_rect

    def set_vel(self, vel):
        self.vel = vel
    
    def set_acc(self, acc):
        self.acc = acc

    def get_xy_velocities(self):
        angleInRadian = math.radians(self.angle)
        vel_x = self.vel * math.cos(angleInRadian)
        vel_y = self.vel * math.sin(angleInRadian)
        return [vel_x, vel_y]
    
    def move(self):
        xy_vel = self.get_xy_velocities()
        if abs(self.vel) < 1:
            if self.vel > 0:
                self.reset()
            self.vel = 0
        else:
            vel_x = xy_vel[0]
            vel_y = xy_vel[1]
            self.rect.x += vel_x
            self.rect.y += vel_y
            self.vel -= self.acc
            self.x = self.rect.x
            self.y = self.rect.y

    def left(self, angle):
        self.angle -= angle

    def right(self, angle):
        self.angle += angle

    def get_angle(self):
        return self.angle

    def increase_launchF(self):
        if self.launchF < 10:
            self.launchF += 1

    def decrease_launchF(self):
        if self.launchF > 0:
            self.launchF -= 1

    def reflect_x(self):
        self.angle = -self.angle

    def reflect_y(self):
        self.angle = 180 - self.angle

    def launch(self, velocity):
        """set initial speed when player launches ball"""
        self.vel = velocity*(1+self.launchF/2)

    def reset(self):
        self.angle = 0
        self.launchF = 0











