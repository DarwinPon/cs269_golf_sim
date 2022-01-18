import pygame
import math

class Consumable:

    def __init__(self, duration):
        self.duration = duration

    def activate(self, plr):
        '''activate the item's effect'''
        pass

    def countdown(self, plr):
        self.duration -= 1
        if self.duration == 0:
            self.deactive(plr)

    def deactivate(self, plr):
        '''deactivate the item's effect'''
        pass


class MassUp(Consumable):
    def __init__(self):
        Consumable.__init__(3)

    def activate(self, plr):
        plr.mass = 3*plr.mass

    def deactivate(self, plr):
        plr.mass = plr.mass/3


class PowerUp(Consumable):
    def __init__(self):
        Consumable.__init__(2)

    def activate(self, plr):
        plr.mass = 3*plr.mass

    def deactivate(self, plr):
        plr.mass = plr.mass/3
