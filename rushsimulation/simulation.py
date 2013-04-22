# Load configs before loading other Kivy stuff. Unfortunately it's the
# only way to ensure that window is not resizable.
from kivy.config import Config
Config.set('graphics', 'resizable', 0)

from kivy.app import App
from kivy.core.window import Window
from kivy.clock import Clock
from kivy.properties import NumericProperty, ObjectProperty
from kivy.uix.widget import Widget

from .vector import Vector
from .vehicle import Vehicle
from .wall import Wall


class RushSimulation(Widget):
    vehicles = []
    simulation_on = False
    start_pause_button = ObjectProperty(None)
    debug_graphic_alpha = NumericProperty(0)
    target = Vector(400, 600)

    def __init__(self, user_configs, *args, **kwargs):
        super(RushSimulation, self).__init__(*args, **kwargs)
        self.user_configs = user_configs
        self.door_size = self.user_configs['Simulation']['doorSize']
        self.vehicle_amount = self.user_configs['Simulation']['vehicleAmount']
        self.debug_graphic_alpha = \
            self.user_configs['Simulation']['debugGraphicAlpha']
        self.wall_1 = Wall(
            user_configs,
            (0, Window.height - 100),
            (Window.width / 2 - self.door_size / 2, 100)
        )
        self.wall_2 = Wall(
            user_configs,
            (Window.width / 2 + self.door_size / 2, Window.height - 100),
            (Window.width / 2 - self.door_size / 2, 100)
        )
        self.add_widget(self.wall_1)
        self.add_widget(self.wall_2)

    def set_up_simulation(self):
        for i in xrange(self.vehicle_amount):
            vehicle = Vehicle(self.user_configs, self.target)
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
                vehicle.move(dt)

    def start_pause_button_pressed(self):
        if self.simulation_on:
            self.pause_simulation()
            self.start_pause_button.text = 'Start'
        else:
            self.start_simulation()
            self.start_pause_button.text = 'Pause'

    def stop_button_pressed(self):
        self.stop_simulation()
        self.start_pause_button.text = 'Start'


class RushApp(App):
    def __init__(self, user_configs, *args, **kwargs):
        super(RushApp, self).__init__(*args, **kwargs)
        self.user_configs = user_configs

    def build(self):
        Window.clearcolor = (0, 0, 0, 1)
        simulation = RushSimulation(user_configs=self.user_configs)
        return simulation
