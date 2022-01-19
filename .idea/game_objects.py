import pygame
import math
import random

class Thing():
    def __init__(self, image, x, y, width, height):
        self.rect = pygame.Rect((x, y), (width, height))
        self.x = x
        self.y = y
        self.width = width
        self.height = height
        self.image = pygame.transform.scale(image, (width, height))

    def get_x(self):
        return self.rect.x

    def get_y(self):
        return self.rect.y

    def get_width(self):
        return self.width

    def get_height(self):
        return self.height

    def get_rect(self):
        return self.rect



class Ball(Thing):
    def __init__(self, image, x, y, width, height, arrow):
        super().__init__(image, x, y, width, height)
        self.vel_x = 0
        self.vel_y = 0
        self.acc = 1
        self.angle = 0
        self.launchF = 0
        self.arrow = arrow
        self.RADIUS = 15
        self.mass = 1
        self.max_power = 10
        self.consumables = []

    def get_consumables(self):
        return self.consumables

    def add_consumable(self, consumable):
        self.consumables.append(consumable)
        
    def remove_consumable(self, consumable):
        self.consumables.remove(consumable)

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


        if abs(vel) < 2:
            if vel > 0:
                self.reset()
            self.set_vel(0)
        else:
            angleInRadian = math.radians(self.angle)
            acc_x = self.acc * math.cos(angleInRadian)


            acc_y = self.acc * math.sin(angleInRadian)

            self.rect.x += self.vel_x
            self.rect.y += self.vel_y
            self.vel_x -= acc_x
            self.vel_y -= acc_y
            self.x = self.rect.x
            self.y = self.rect.y



    def advance(self):
        '''allows the ball to take a step forward without changing its speed. Only used in collision detection'''

        self.x += self.vel_x
        self.y += self.vel_y


    def trace_back(self):
        '''allows the ball to take a step back. Only used in collision detection'''
        self.x -= self.vel_x
        self.y -= self.vel_y


    def left(self, angle):
        self.angle -= angle

    def right(self, angle):
        self.angle += angle

    def get_angle(self):
        return self.angle

    def increase_launchF(self):

        if self.launchF < self.max_power:
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
        self.angle = math.degrees(math.atan2(self.vel_y, self.vel_x))

    def reset(self):
        self.angle = 0
        self.launchF = 0

class Arrow(Thing):
    def __init__(self, image, x, y, width, height):
        super().__init__(image, x, y, width, height)
        self.rot_img = image
        self.rot_rect = self.rect.copy()
        self.is_visible = True

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


class Consumable(Thing):
    def __init__(self, duration, image, x, y, width, height):
        super().__init__(image, x, y, width, height)
        self.duration = duration

    def get_duration(self):
        return self.duration
    
    def set_duration(self, new_duration):
        self.duration = new_duration

    def need_to_deactivate(self):
        if self.duration == 0:
            return True
        else:
            self.duration -= 1
            return False

    def activate(self, plr):
        '''activate the item's effect'''
        pass

    def deactivate(self, plr):
        '''deactivate the item's effect'''
        pass


class MassUp(Consumable):
    def __init__(self, image, x, y, width, height):
        super().__init__(3, image, x, y, width, height)

    def activate(self, plr):
        plr.mass = 3*plr.mass

    def deactivate(self, plr):
        plr.mass = plr.mass/3


class PowerUp(Consumable):
    def __init__(self, image, x, y, width, height):
        super().__init__(2, image, x, y, width, height)

    def activate(self, plr):
        plr.max_power = 20

    def deactivate(self, plr):
        plr.max_power = 10


class SpeedUp(Consumable):
    def __init__(self, image, x, y, width, height):
        super().__init__(2, image, x, y, width, height)

    def activate(self, plr):
        plr.acc /= 3

    def deactivate(self, plr):
        plr.acc *= 3


class RandomAngle(Consumable):
    def __init__(self, image, x, y, width, height):
        super().__init__(1, image, x, y, width, height)

    def activate(self, plr):
        plr.angle = random.randint(0, 360)

    def deactivate(self, plr):
        plr.angle = 0










