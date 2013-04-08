from kivy.uix.widget import Widget


class Wall(Widget):

    def __init__(self, pos, size, *args, **kwargs):
        super(Wall, self).__init__(*args, **kwargs)
        self.pos = pos
        self.size = size
