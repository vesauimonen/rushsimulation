import kivy
kivy.require('1.5.1')

from kivy.app import App
from kivy.uix.widget import Widget


class RushSimulation(Widget):
    pass


class RushApp(App):
    def build(self):
        return RushSimulation()

if __name__ == '__main__':
    RushApp().run()
