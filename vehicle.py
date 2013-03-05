from kivy.uix.widget import Widget
from kivy.vector import Vector


class Vehicle(Widget):
    velocity = Vector(0, 0)
    target = Vector(400, 600)

    def move(self):
        self.velocity = -Vector(self.x, self.y) + self.target
        self.velocity = self.velocity.normalize() * 5
        self.pos = Vector(*self.velocity) + self.pos

    def is_in_target(self):
        offset = 5
        return self.x < self.target.x + offset and\
            self.x > self.target.x - offset and\
            self.y < self.target.y + offset and self.y > self.target.y - offset
