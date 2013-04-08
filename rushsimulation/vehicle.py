from random import randint

from kivy.uix.widget import Widget
from kivy.utils import interpolate
from .vector import Vector


class Vehicle(Widget):
    TARGET_OFFSET = 10
    SEPARATION_WEIGHT = 10
    velocity = Vector(0, 0)
    acceleration = Vector(0, 0)
    steering_force = Vector(0, 0)
    max_force = 7
    max_speed = 4
    radius = 8
    mass = 10

    def __init__(self, target_vector=Vector(400, 600), *args, **kwargs):
        super(Vehicle, self).__init__(*args, **kwargs)
        self.target = target_vector

    def move(self):
        self.steering_force = self.get_overall_steering_force()
        self.acceleration = self.steering_force / self.mass
        self.velocity = self.velocity + self.acceleration
        self.velocity = Vector(*self.velocity).truncate(self.max_speed)
        self.pos = interpolate(self.pos, self.velocity + self.pos, 2)

    def set_to_start_position(self):
        self.pos = Vector(randint(0, 800), 0)
        self.max_speed = randint(3, 5)
        self.velocity = Vector(0, 0)
        self.acceleration = Vector(0, 0)
        self.steering_force = Vector(0, 0)

    def is_in_target(self):
        return self.x <= self.target.x + self.TARGET_OFFSET and\
            self.x >= self.target.x - self.TARGET_OFFSET and\
            self.y <= self.target.y + self.TARGET_OFFSET and\
            self.y >= self.target.y - self.TARGET_OFFSET

    def get_overall_steering_force(self):
        # if self.get_braking_force() != Vector(0, 0):
        #     return self.get_braking_force()
        return 0.5 * self.get_seeking_force() + self.get_separation_force()

    def get_nearby_vehicles(self):
        nearby_vehicles = []
        for vehicle in self.parent.vehicles:
            distance = Vector(self.pos).distance(vehicle.pos)
            if vehicle is not self and distance <= 50:
                nearby_vehicles.append(vehicle)
        return nearby_vehicles

    def get_vehicles_in_front_of(self):
        vehicles_in_front_of = []
        for vehicle in self.parent.vehicles:
            direction = -Vector(self.pos) + Vector(vehicle.pos)
            angle = self.velocity.angle(direction)
            if vehicle is not self and direction.length() <= 50 and angle > -90 and angle < 90:
                vehicles_in_front_of.append(vehicle)
        return vehicles_in_front_of

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

    def get_separation_force(self):
        sum_force = Vector(0, 0)
        for vehicle in self.get_nearby_vehicles():
            direction = Vector(self.pos) - Vector(vehicle.pos)
            distance = Vector(self.pos).distance(vehicle.pos)
            if distance != 0:
                sum_force = sum_force + direction * (1 / distance ** 2) * self.SEPARATION_WEIGHT
        sum_force = Vector(*sum_force).truncate(self.max_force)
        return sum_force

    def get_wall_avoiding_force(self):
        # Todo
        pass

    def get_braking_force(self):
        for vehicle in self.get_vehicles_in_front_of():
            if vehicle.velocity.length() < self.velocity.length():
                return -Vector(self.steering_force)
        return Vector(0, 0)
