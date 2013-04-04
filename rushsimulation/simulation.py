from kivy.app import App
from kivy.core.window import Window
from kivy.clock import Clock
from kivy.properties import ObjectProperty
from kivy.uix.widget import Widget

from .vector import Vector
from .vehicle import Vehicle


class RushSimulation(Widget):
    VEHICLE_AMOUNT = 5
    Window.clearcolor = (.9, .9, .9, 1)
    vehicles = []
    simulation_on = False
    start_pause_button = ObjectProperty(None)

    def set_up_simulation(self):
        for i in xrange(self.VEHICLE_AMOUNT):
            vehicle = Vehicle(Vector(400, 600))
            self.add_widget(vehicle)
            self.vehicles.append(vehicle)
            vehicle.set_to_start_position()

    def start_simulation(self):
        if len(self.vehicles) == 0:
            self.set_up_simulation()
        Clock.schedule_interval(self.update, 1.0 / 60.0)
        self.simulation_on = True

    def pause_simulation(self):
        Clock.unschedule(self.update)
        self.simulation_on = False

    def stop_simulation(self):
        if self.simulation_on:
            self.pause_simulation()
        self.remove_all_vehicles()

    def add_vehicle(self, vehicle):
        self.add_widget(vehicle)
        self.vehicles.append(vehicle)

    def remove_vehicle(self, vehicle):
        self.remove_widget(vehicle)
        self.vehicles.remove(vehicle)
        vehicle = None

    def remove_all_vehicles(self):
        for vehicle in self.vehicles:
            self.remove_widget(vehicle)
        self.vehicles = []

    def update(self, dt):
        for vehicle in self.vehicles:
            if vehicle.is_in_target():
                vehicle.set_to_start_position()
            else:
                vehicle.move()

    def start_pause_button_pressed(self):
        if self.simulation_on:
            self.pause_simulation()
            self.start_pause_button.text = 'Start'
        else:
            self.start_simulation()
            self.start_pause_button.text = 'Pause'

    def stop_button_pressed(self):
        self.stop_simulation()


class RushApp(App):
    def build(self):
        simulation = RushSimulation()
        return simulation
