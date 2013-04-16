from kivy.uix.widget import Widget

from .vector import Vector


class Wall(Widget):

    def __init__(self, pos, size, *args, **kwargs):
        super(Wall, self).__init__(*args, **kwargs)
        self.pos = pos
        self.size = size

    def get_collision_point(self, tip, pos):
        '''
        Calculates a point in the wall edge which is between points tip and
        pos.
        '''
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

    def is_between_points(self, a, b, c):
        '''
        Determines if point c is between points a and b. Assumes that all the
        points are aligned.
        '''
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
        '''
        Determines if the point is within the wall.
        '''
        inside_x = point[0] >= self.x and point[0] <= self.x + self.width
        inside_y = point[1] >= self.y and point[1] <= self.y + self.height
        return inside_x and inside_y
