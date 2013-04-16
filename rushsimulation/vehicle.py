from random import randint

from kivy.uix.widget import Widget
from kivy.utils import interpolate

from .vector import Vector


class Vehicle(Widget):
    TARGET_OFFSET = 10
    NEARBY_OFFSET = 50
    IN_FRONT_OF_OFFSET = 50
    IN_FRONT_OF_ANGLE = 120
    OBSTACLE_AVOIDANCE_ANGLE = 70
    SEPARATION_WEIGHT = 100
    SEEKING_WEIGHT = 1
    BRAKING_RATE = 5.25
    velocity = Vector(0, 0)
    acceleration = Vector(0, 0)
    steering_force = Vector(0, 0)
    obstacle_avoider = Vector(0, 0)

    def __init__(self, user_configs, target_vector, *args, **kwargs):
        super(Vehicle, self).__init__(*args, **kwargs)
        self.user_configs = user_configs
        self.max_speed = self.user_configs['Vehicle']['maxSpeed']
        self.max_force = self.user_configs['Vehicle']['maxForce']
        self.mass = self.user_configs['Vehicle']['mass']
        self.diameter = self.user_configs['Vehicle']['diameter']
        self.target = target_vector
        self.size = (self.diameter, self.diameter)

    def set_to_start_position(self):
        self.pos = Vector(randint(0, 800), 0)
        self.max_speed = randint(3, 8)
        self.velocity = Vector(0, 0)
        self.acceleration = Vector(0, 0)
        self.steering_force = Vector(0, 0)

    def is_in_target(self):
        return self.x <= self.target.x + self.TARGET_OFFSET and\
            self.x >= self.target.x - self.TARGET_OFFSET and\
            self.y <= self.target.y + self.TARGET_OFFSET and\
            self.y >= self.target.y - self.TARGET_OFFSET

    def move(self, dt):
        self.velocity = self.calculate_new_velocity(dt)
        self.obstacle_avoider = self.calculate_new_obstacle_avoider()
        self.pos = interpolate(self.pos, self.velocity + self.pos, 2)

    def calculate_new_velocity(self, dt):
        distance = self.get_distance_to_slow_vehicle()
        if distance < self.IN_FRONT_OF_OFFSET:
            return self.brake(distance, dt)
        else:
            self.steering_force = self.get_overall_steering_force()
            self.acceleration = self.steering_force / self.mass
            velocity = self.velocity + self.acceleration
            velocity = Vector(velocity).truncate(self.max_speed)
            return velocity

    def calculate_new_obstacle_avoider(self):
        return (self.velocity.normalize().rotate(randint(
            -self.OBSTACLE_AVOIDANCE_ANGLE / 2,
            self.OBSTACLE_AVOIDANCE_ANGLE / 2
        )) * 20)

    def brake(self, distance, dt):
        if distance <= self.diameter + 4:
            return Vector(0, 0)
        speed = self.velocity.length()
        raw_braking = speed * self.BRAKING_RATE
        raw_braking *= (self.IN_FRONT_OF_OFFSET / distance)
        if raw_braking < self.max_force:
            clip_braking = raw_braking
        else:
            clip_braking = self.max_force

        return self.velocity.normalize() * (speed - (clip_braking * dt))

    def get_overall_steering_force(self):
        return (
            self.get_seeking_force() * self.SEEKING_WEIGHT +
            self.get_separation_force() * self.SEPARATION_WEIGHT
        )

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
        nearby_vehicles = self.get_nearby_vehicles(
            self.NEARBY_OFFSET
        )
        for vehicle in nearby_vehicles:
            direction = Vector(self.pos) - Vector(vehicle.pos)
            distance = Vector(self.pos).distance(vehicle.pos)
            if distance != 0:
                sum_force = sum_force + direction * (1 / distance ** 2)
        sum_force = Vector(*sum_force).truncate(self.max_force)
        return sum_force

    def get_wall_avoiding_force(self):
        # Todo
        pass

    def get_distance_to_slow_vehicle(self):
        vehicles_in_front_of = self.get_vehicles_in_front_of(
            self.IN_FRONT_OF_OFFSET,
            self.IN_FRONT_OF_ANGLE
        )
        smallest_distance = self.IN_FRONT_OF_OFFSET
        for vehicle in vehicles_in_front_of:
            distance = Vector(self.pos).distance(vehicle.pos)
            speed = vehicle.velocity.length()
            if (speed < self.velocity.length() and
                    distance < smallest_distance):
                smallest_distance = distance
        return smallest_distance

    def get_nearby_vehicles(self, boundary):
        nearby_vehicles = []
        for vehicle in self.parent.vehicles:
            distance = Vector(self.pos).distance(vehicle.pos)
            if vehicle is not self and distance <= boundary:
                nearby_vehicles.append(vehicle)
        return nearby_vehicles

    def get_vehicles_in_front_of(self, boundary, angle_boundary):
        vehicles_in_front_of = []
        for vehicle in self.parent.vehicles:
            direction = -Vector(self.pos) + Vector(vehicle.pos)
            if vehicle is self or direction.length() > boundary:
                continue
            within_angle = self.vectors_are_within_angular_range(
                self.velocity, direction, angle_boundary
            )
            if within_angle:
                vehicles_in_front_of.append(vehicle)
        return vehicles_in_front_of

    def vectors_are_within_angular_range(self, vector_1, vector_2, angle):
        real_angle = vector_1.angle(vector_2)
        return real_angle > -angle / 2 and real_angle < angle / 2
