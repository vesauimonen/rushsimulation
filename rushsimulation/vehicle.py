from random import randint

from kivy.core.window import Window
from kivy.properties import NumericProperty
from kivy.uix.widget import Widget
from kivy.utils import interpolate

from .vector import Vector


class Vehicle(Widget):
    # Constants
    TARGET_OFFSET = 10
    NEARBY_OFFSET = 50
    START_POSITION_RADIUS = 500
    START_POSITION_ANGLE = 130
    IN_FRONT_OF_OFFSET = 50
    IN_FRONT_OF_ANGLE = 100
    WALL_AVOIDANCE_ANGLE = 20
    WALL_AVOIDANCE_OFFSET = 120
    SEPARATION_WEIGHT = 100
    SEEKING_WEIGHT = 1
    BRAKING_RATE = 0.3
    MASS = 15
    # Initialized, so .kv can use these
    debug_graphic_alpha = NumericProperty(0)
    velocity = Vector(0, 0)
    acceleration = Vector(0, 0)
    steering_force = Vector(0, 0)
    lookup_point = Vector(0, 0)
    collision = Vector(0, 0)

    def __init__(self, user_configs, target_vector, *args, **kwargs):
        super(Vehicle, self).__init__(*args, **kwargs)
        self.user_configs = user_configs
        self.user_max_speed = self.user_configs['Vehicle']['maxSpeed']
        self.max_force = self.user_configs['Vehicle']['maxForce']
        self.diameter = self.user_configs['Vehicle']['diameter']
        self.debug_graphic_alpha = \
            self.user_configs['Simulation']['debugGraphicAlpha']
        self.target = target_vector
        self.size = (self.diameter, self.diameter)

    def set_to_start_position(self):
        self.pos = self.calculate_start_position()
        self.max_speed = randint(4, self.user_max_speed)
        self.velocity = Vector(0, 0)
        self.acceleration = Vector(0, 0)
        self.steering_force = Vector(0, 0)
        self.lookup_point = self.pos

    def calculate_start_position(self):
        """
        Calculates a new start position around a circle centered in the target.
        """
        rotator = self.target - \
            Vector(self.target[0], Window.height - self.START_POSITION_RADIUS)
        rotator = rotator.rotate(randint(
            -self.START_POSITION_ANGLE / 2,
            self.START_POSITION_ANGLE / 2
        ))
        return self.target - rotator

    def is_in_target(self):
        """
        Determines if the vehicle has reached its target or is outside the top
        of the window.
        """
        within_offset = self.x <= self.target.x + self.TARGET_OFFSET and\
            self.x >= self.target.x - self.TARGET_OFFSET and\
            self.y <= self.target.y + self.TARGET_OFFSET and\
            self.y >= self.target.y - self.TARGET_OFFSET
        out_of_top = self.top > Window.height
        if within_offset or out_of_top:
            return True
        return False

    def move(self, dt):
        """
        Moves the vehicle according to Simple Vehicle Model principles.
        This method is called by self.parent repeatedly.
        """
        self.calculate_new_lookup_point()
        self.velocity = self.calculate_new_velocity()
        new_pos = self.validate_pos(self.velocity + self.pos)
        self.pos = interpolate(self.pos, new_pos, 3)

    def validate_pos(self, pos):
        """
        Tries to ensure that two vehicles don't overlap. Calculates distance
        between vehicles and moves self.pos accordingly.
        """
        for vehicle in self.parent.vehicles:
            if vehicle is self:
                continue
            if Vector(pos).distance(vehicle.pos) < self.diameter:
                offset = Vector(pos) - Vector(vehicle.pos)
                offset = Vector(offset).normalize() * self.diameter
                return Vector(vehicle.pos) + Vector(offset)
        return pos

    def calculate_new_velocity(self):
        """
        Calculates a new velocity for the vehicle. If slower vehicles are
        nearby, braking occurs. Otherwise steering force is used for
        the new velocity.
        """

        # Allowing an 20% chance of not checking the need for braking
        if randint(0, 10) > 1:
            distance = self.get_distance_to_slow_vehicle()
            if distance < self.IN_FRONT_OF_OFFSET:
                return self.brake(self.velocity, distance)
        self.steering_force = self.get_overall_steering_force()
        self.acceleration = self.steering_force / self.MASS
        velocity = self.velocity + self.acceleration
        velocity = Vector(velocity).truncate(self.max_speed)
        return velocity

    def calculate_new_lookup_point(self):
        """
        Returns a random point in front of the vehicle within a certain angle
        and distance.
        """
        offset = self.velocity.normalize()
        offset_center = offset.rotate(randint(
            -self.WALL_AVOIDANCE_ANGLE / 2,
            self.WALL_AVOIDANCE_ANGLE / 2
        ))
        offset_center *= self.WALL_AVOIDANCE_OFFSET
        self.lookup_point = (
            self.pos[0] + offset_center[0],
            self.pos[1] + offset_center[1]
        )

    def brake(self, velocity, distance):
        """
        Returns a velocity less than current velocity, thus simulating
        a braking behaviour. The closer the nearby vehicle is the greater the
        decrease of the velocity is.
        """
        speed = velocity.length()
        raw_braking = speed * self.BRAKING_RATE
        raw_braking *= (self.IN_FRONT_OF_OFFSET / distance)
        if raw_braking < self.max_force:
            clip_braking = raw_braking
        else:
            clip_braking = self.max_force
        return velocity.normalize() * (speed - (clip_braking))

    def get_overall_steering_force(self):
        """
        Returns an overall force which simulates different behaviours of the
        Simple Vehicle Model. Wall avoidance is prioritized over other
        behaviours.
        """
        wall_avoiding_force = self.get_wall_avoiding_force()
        if wall_avoiding_force.length() > 0:
            return wall_avoiding_force
        return (
            self.get_seeking_force() * self.SEEKING_WEIGHT +
            self.get_separation_force() * self.SEPARATION_WEIGHT
        )

    def get_seeking_force(self):
        """
        Calculates the force related to the seeking behaviour of the Simple
        Vehicle Model.
        """
        desired_direction = Vector(
            self.target[0] - self.pos[0],
            self.target[1] - self.pos[1]
        )
        force = desired_direction.truncate(self.max_force)
        return self.velocity + force

    def get_separation_force(self):
        """
        Calculates the force related to the separation behaviour of the Simple
        Vehicle Model.
        """
        sum_force = Vector(0, 0)
        nearby_vehicles = self.get_nearby_vehicles(self.NEARBY_OFFSET)
        for vehicle in nearby_vehicles:
            direction = Vector(self.pos) - Vector(vehicle.pos)
            distance = Vector(self.pos).distance(vehicle.pos)
            if distance != 0:
                sum_force = sum_force + direction * (1 / distance ** 2)
        sum_force = Vector(sum_force).truncate(self.max_force)
        return sum_force

    def get_wall_avoiding_force(self):
        """
        Calculates a force to achieve wall avoidance. Looks up possible
        collision point with both of the walls and deteremines which of them is
        closer and uses that one to calculate a force.
        """
        collision_1 = self.parent.wall_1.get_collision_point(
            self.lookup_point,
            self.pos
        )
        collision_2 = self.parent.wall_2.get_collision_point(
            self.lookup_point,
            self.pos
        )
        if collision_1 and collision_2:
            distance_1 = Vector(self.pos).distance(collision_1)
            distance_2 = Vector(self.pos).distance(collision_2)
            if distance_1 >= distance_2:
                collision_1 = None
        if collision_1:
            return self.get_force_outwards_from_wall(
                collision_1, -90
            )
        if collision_2:
            return self.get_force_outwards_from_wall(
                collision_2, 90
            )
        return Vector(0, 0)

    def get_force_outwards_from_wall(self, collision, angle):
        """
        Calculates a force to steer away from collision point,
        with given angle.
        """
        distance = Vector(self.pos).distance(collision)
        weight = self.WALL_AVOIDANCE_OFFSET / distance
        direction = Vector(
            collision[0] - self.pos[0],
            collision[1] - self.pos[1]
        )
        direction = direction.normalize().rotate(angle)
        return direction * self.max_force * weight

    def get_distance_to_slow_vehicle(self):
        """
        Returns the distance to the closest vehicle in front of us that has
        a smaller speed than us.
        """
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
        """
        Returns vehicles that are within the given boundary distance.
        """
        nearby_vehicles = []
        for vehicle in self.parent.vehicles:
            distance = Vector(self.pos).distance(vehicle.pos)
            if vehicle is not self and distance <= boundary:
                nearby_vehicles.append(vehicle)
        return nearby_vehicles

    def get_vehicles_in_front_of(self, boundary, angle_boundary):
        """
        Returns vehicles that are in front of and within the given boundary
        distance and angle.
        """
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
        """
        Helper method for comparing the angluar range of two vectors.
        """
        real_angle = vector_1.angle(vector_2)
        return real_angle > -angle / 2 and real_angle < angle / 2
