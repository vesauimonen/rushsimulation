from kivy.app import App
from kivy.uix.widget import Widget
from kivy.core.window import Window
from kivy.clock import Clock
from .vector import Vector
from .vehicle import Vehicle


class RushSimulation(Widget):
    VEHICLE_AMOUNT = 20
    Window.clearcolor = (.9, .9, .9, 1)
    vehicles = []

    def start_simulation(self):
        for i in xrange(self.VEHICLE_AMOUNT):
            vehicle = Vehicle(Vector(400, 600))
            vehicle.set_to_start_position()
            self.add_widget(vehicle)
            self.vehicles.append(vehicle)
        Clock.schedule_interval(self.update, 1.0 / 60.0)

    def update(self, dt):
        for vehicle in self.vehicles:
            if vehicle.is_in_target():
                vehicle.set_to_start_position()
            else:
                vehicle.move()


class RushApp(App):
    def build(self):
        simulation = RushSimulation()
        simulation.start_simulation()
        return simulation
