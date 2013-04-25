from kivy.properties import NumericProperty
from kivy.uix.widget import Widget

from .vector import Vector


class Wall(Widget):
    debug_graphic_alpha = NumericProperty(0)

    def __init__(self, user_configs, pos, size, *args, **kwargs):
        super(Wall, self).__init__(*args, **kwargs)
        self.user_configs = user_configs
        self.pos = pos
        self.size = size
        self.debug_graphic_alpha = \
            self.user_configs['Simulation']['debugGraphicAlpha']

    def get_collision_point(self, tip, pos):
        """
        Returns a collision point of the line going through tip and pos and
        the edges of this wall.
        """
        collison_point_x = self.get_collision_point_x(tip, pos)
        collison_point_y = self.get_collision_point_y(tip, pos)
        if collison_point_x and collison_point_y:
            distance_x = Vector(pos).distance(collison_point_x)
            distance_y = Vector(pos).distance(collison_point_y)
            if distance_x < distance_y:
                return collison_point_x
            return collison_point_y
        elif collison_point_x:
            return collison_point_x
        return collison_point_y

    def get_collision_point_x(self, tip, pos):
        """
        Calculates a point in the x aligned edge of the wall. The point must be
        between points tip and pos.
        """
        y = self.y
        if (pos[1] - tip[1]) != 0:
            inverse_k = float(pos[0] - tip[0]) / float(pos[1] - tip[1])
            x = inverse_k * (y - pos[1]) + pos[0]
        else:
            x = pos[0]
        point = Vector(x, y)
        if self.is_inside(point) and self.is_between_points(pos, tip, point):
            return point
        return None

    def get_collision_point_y(self, tip, pos):
        """
        Calculates a point in the y aligned edge of the wall. The point must be
        between points tip and pos.
        """
        x = self.x
        # Hack to identify that this is wall no. 1
        if self.x == 0:
            x += self.width
        if (pos[0] - tip[0]) != 0:
            k = float(pos[1] - tip[1]) / float(pos[0] - tip[0])
            y = k * (x - pos[0]) + pos[1]
        else:
            y = pos[1]
        point = Vector(x, y)
        if self.is_inside(point) and self.is_between_points(pos, tip, point):
            return point
        return None

    def is_between_points(self, a, b, c):
        """
        Determines if point c is between points a and b. Assumes that all the
        points are aligned.
        """
        # Dot product of (b-a) and (c-a)
        dot = (c[0] - a[0]) * (b[0] - a[0]) + (c[1] - a[1]) * (b[1] - a[1])
        if dot < 0:
            return False
        # The square of the distance between a and b
        squared_length = (b[0] - a[0]) * (b[0] - a[0])
        squared_length += (b[1] - a[1]) * (b[1] - a[1])
        if dot > squared_length:
            return False
        return True

    def is_inside(self, point):
        """
        Determines if the point is within the wall.
        """
        inside_x = point[0] >= self.x and point[0] <= self.x + self.width
        inside_y = point[1] >= self.y and point[1] <= self.y + self.height
        return inside_x and inside_y
