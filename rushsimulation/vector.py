from kivy.vector import Vector as BaseVector


class Vector(BaseVector):
    """
    Extends Kivy's Vector class with a truncate method.
    """
    def __init__(self, *largs):
        super(Vector, self).__init__(*largs)

    def truncate(self, limit):
        """
        Truncate vector by limit.
        """
        if self.length() > limit:
            return self.normalize() * limit
        return self
