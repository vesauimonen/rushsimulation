from random import randint

from kivy.uix.widget import Widget
from kivy.vector import Vector


class Vehicle(Widget):
    TARGET_OFFSET = 5
    velocity = Vector(0, 0)
    acceleration = Vector(0, 0)
    target = Vector(400, 600)
    steering_force = Vector(0, 0)
    max_force = 10
    max_speed = 10
    radius = 8
    mass = 10

    def __init__(self, target_vector=Vector(400, 600), *args, **kwargs):
        super(Vehicle, self).__init__(*args, **kwargs)
        self.target = target_vector

    def move(self):
        self.velocity = self.get_overall_steering_force()
        self.pos = Vector(*self.velocity) + self.pos

    def is_in_target(self):
        return self.x <= self.target.x + self.TARGET_OFFSET and\
            self.x >= self.target.x - self.TARGET_OFFSET and\
            self.y <= self.target.y + self.TARGET_OFFSET and\
            self.y >= self.target.y - self.TARGET_OFFSET

    def set_to_start_position(self):
        pos = Vector(randint(0, 800), 0)
        self.pos = pos

    def get_overall_steering_force(self):
        force = -Vector(self.x, self.y) + self.target
        return force.normalize() * self.max_force

    def get_vehicles_nearby(self):
        # Todo
        pass

    def get_separation_force(self):
        # Todo
        pass

    def get_seeking_force(self):
        # Todo
        pass

    def get_wall_avoiding_force(self):
        # Todo
        pass

    def get_braking_force(self):
        # Todo
        pass
