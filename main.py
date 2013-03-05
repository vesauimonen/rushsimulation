from kivy.app import App
from kivy.uix.widget import Widget
from kivy.core.window import Window
from kivy.properties import ObjectProperty
from kivy.clock import Clock
from kivy.factory import Factory
from kivy.vector import Vector
from vehicle import Vehicle
from random import randint


class RushSimulation(Widget):
    Window.clearcolor = (.9, .9, .9, 1)
    vehicles = []

    def start_simulation(self):
        for i in xrange(10):
            temp_vehicle = Vehicle()
            temp_vehicle.target = Vector(400, 600)
            self.add_widget(temp_vehicle)
            self.vehicles.append(temp_vehicle)
        Clock.schedule_interval(self.update, 1.0 / 60.0)

    def update(self, dt):
        for vehicle in self.vehicles:
            if vehicle.is_in_target():
                pos = Vector(randint(0, 800), 0)
                vehicle.center = pos
            else:
                vehicle.move()




class RushApp(App):
    def build(self):
        simulation = RushSimulation()
        simulation.start_simulation()

        return simulation

if __name__ == '__main__':
    RushApp().run()
