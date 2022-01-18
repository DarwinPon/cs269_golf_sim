
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
        self.vel_x = 0
        self.vel_y = 0
        self.acc = 0.25
        self.angle = 0
        self.launchF = 0
        self.arrow = arrow
        self.RADIUS = 15
        self.mass = 1
        self.max_powe = 10

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
        angleInRadian = math.radians(self.angle)
        self.vel_x = vel * math.cos(angleInRadian)
        self.vel_y = vel * math.sin(angleInRadian)
    
    def set_acc(self, acc):
        self.acc = acc

    def get_xy_velocities(self):
        return [self.vel_x, self.vel_y]

    def get_vel(self):
        return math.hypot(self.vel_x, self.vel_y)
    
    def move(self):

        vel = self.get_vel()
        if abs(vel) < 1:
            if vel > 0:
                self.reset()
            self.set_vel(0)
        else:
            angleInRadian = math.radians(self.angle)
            acc_x = self.acc * math.cos(angleInRadian)

            acc_y = self.acc * math.sin(angleInRadian)
            print(acc_y)
            self.rect.x += self.vel_x
            self.rect.y += self.vel_y
            self.vel_x -= acc_x
            self.vel_y -= acc_y
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
        self.vel_y = -self.vel_y

    def reflect_y(self):
        self.angle = 180 - self.angle
        self.vel_x = -self.vel_x

    def launch(self, velocity):
        """set initial speed when player launches ball"""
        vel = velocity*(1+self.launchF/2)
        angleInRadian = math.radians(self.angle)
        self.vel_x = vel * math.cos(angleInRadian)
        self.vel_y = vel * math.sin(angleInRadian)

    def update_angle(self):
        self.angle = math.degrees(-math.atan2(self.vel_y, self.vel_x))

    def reset(self):
        self.angle = 0
        self.launchF = 0











