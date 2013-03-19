from random import randint

from kivy.uix.widget import Widget
from .vector import Vector


class Vehicle(Widget):
    TARGET_OFFSET = 5
    velocity = Vector(0, 0)
    acceleration = Vector(0, 0)
    steering_force = Vector(0, 0)
    max_force = 7
    max_speed = 6
    radius = 8
    mass = 10

    def __init__(self, target_vector=Vector(400, 600), *args, **kwargs):
        super(Vehicle, self).__init__(*args, **kwargs)
        self.target = target_vector
        self.set_to_start_position()

    def move(self):
        self.steering_force = self.get_overall_steering_force()
        self.acceleration = self.steering_force / self.mass
        self.velocity = self.velocity + self.acceleration
        self.velocity = self.velocity.normalize() * self.max_speed
        self.pos = self.velocity + self.pos

    def is_in_target(self):
        return self.x <= self.target.x + self.TARGET_OFFSET and\
            self.x >= self.target.x - self.TARGET_OFFSET and\
            self.y <= self.target.y + self.TARGET_OFFSET and\
            self.y >= self.target.y - self.TARGET_OFFSET

    def set_to_start_position(self):
        self.pos = Vector(randint(0, 800), 0)
        self.velocity = Vector(0, 0)
        self.acceleration = Vector(0, 0)
        self.steering_force = Vector(0, 0)

    def get_overall_steering_force(self):
        return self.get_seeking_force()

    def get_vehicles_nearby(self):
        # Todo
        pass

    def get_separation_force(self):
        # Todo
        pass

    def get_seeking_force(self):
        '''
        Calculates the force related to the seeking behaviour of the vehicle.
        '''
        # Vector from vehicle position towards target
        desired_velocity = Vector(
            self.target[0] - self.pos[0],
            self.target[1] - self.pos[1]
        )
        desired_force = desired_velocity.truncate(self.max_force)
        return self.velocity + desired_force

    def get_wall_avoiding_force(self):
        # Todo
        pass

    def get_braking_force(self):
        # Todo
        pass
